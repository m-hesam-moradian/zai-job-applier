import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

from src.schemas.models import DynamicCandidateProfile, JobPosting
from src.tailor.document_tailor import tailor_application_for_job, compile_application_pdfs
from src.tailor.cv_template import render_cv_html

async def main():
    profile_path = Path("F:/talentflow-ai/data/ultimate_profile.json")
    profile = DynamicCandidateProfile.model_validate(json.loads(profile_path.read_text(encoding="utf-8")))

    # Load 5U AI job description
    with open("F:/talentflow-ai/JD-Datasets/linkedin_selected_jobs_2026-10-20.json", encoding="utf-8") as f:
        jobs = json.load(f)

    job_raw = next(j for j in jobs if str(j.get("jobId") or j.get("id")) == "4461009898")
    job = JobPosting(
        id="4461009898",
        title="Full-Stack AI Engineer",
        company="5U AI",
        location="Munich, Bavaria, Germany (Onsite)",
        description=job_raw.get("description", ""),
        url=job_raw.get("applyUrl") or job_raw.get("url", ""),
    )

    pkg = tailor_application_for_job(job, profile)
    print(f"Tailored for {job.company} - Match score: {pkg.match_score}%")
    print(f"Headline: {pkg.tailored_headline}")
    print(f"Top Skills: {', '.join(pkg.selected_skills[:10])}")

    out_dir = Path("F:/talentflow-ai/output/5U_AI_4461009898")
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generate CV HTML & PDF
    html_content = render_cv_html(profile, pkg)
    html_file = out_dir / "cv_tailored.html"
    html_file.write_text(html_content, encoding="utf-8")

    pdf_file = out_dir / "Sam_Moradian_CV.pdf"
    preview_png = out_dir / "Sam_Moradian_CV_preview.png"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({"width": 794, "height": 1123})
        await page.goto(html_file.as_uri(), wait_until="networkidle")

        await page.pdf(
            path=str(pdf_file),
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
        )
        await page.screenshot(path=str(preview_png), full_page=False)
        await browser.close()

    print(f"CV PDF generated: {pdf_file} ({pdf_file.stat().st_size} bytes)")

    # 2. Compile Motivation Letter PDF
    pdf_paths = compile_application_pdfs(pkg, profile, Path("F:/talentflow-ai/output"))
    print(f"PDFs compiled: {pdf_paths}")

    # Copy to stage temp files for easy upload
    import shutil
    temp_cv = Path("C:/Users/Sam/AppData/Local/Temp/5U_AI_CV.pdf")
    shutil.copyfile(pdf_file, temp_cv)
    print(f"Staged CV to {temp_cv}")

    # Save motivation letter text
    txt_path = out_dir / "Sam_Moradian_Motivation_Letter.txt"
    txt_path.write_text(pkg.motivation_letter, encoding="utf-8")
    print(f"Saved motivation letter text: {txt_path}")

if __name__ == "__main__":
    asyncio.run(main())
