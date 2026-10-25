import asyncio
import json
import shutil
from pathlib import Path
from playwright.async_api import async_playwright

from src.schemas.models import DynamicCandidateProfile, JobPosting
from src.tailor.document_tailor import tailor_application_for_job, compile_application_pdfs
from src.tailor.cv_template import render_cv_html

async def main():
    profile_path = Path("F:/talentflow-ai/data/ultimate_profile.json")
    profile = DynamicCandidateProfile.model_validate(json.loads(profile_path.read_text(encoding="utf-8")))

    # Load TODAY job description
    with open("F:/talentflow-ai/JD-Datasets/linkedin_selected_jobs_2026-10-20.json", encoding="utf-8") as f:
        jobs = json.load(f)

    today_raw = next(j for j in jobs if str(j.get("jobId") or j.get("id")) == "4476999812")
    job = JobPosting(
        id="4476999812",
        title=today_raw.get("title", "Senior Fullstack Engineer: AI, Backend, Infrastructure"),
        company="TODAY",
        location=today_raw.get("location", "Berlin, Berlin, Germany"),
        description=today_raw.get("description", ""),
        url=today_raw.get("applyUrl") or today_raw.get("url", ""),
    )

    # Tailor package specifically for TODAY JD
    pkg = tailor_application_for_job(job, profile)
    print(f"Tailored for {job.company} - Match score: {pkg.match_score}%")
    print(f"Headline: {pkg.tailored_headline}")
    print(f"Top Skills: {', '.join(pkg.selected_skills[:10])}")

    out_dir = Path("F:/talentflow-ai/output/TODAY_4476999812")
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generate HTML & PDF with Playwright
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
    ml_pdf = pdf_paths.get("motivation_pdf")
    print(f"ML PDF generated: {ml_pdf}")

    # 3. Stage files in Temp directory for upload
    temp_cv = Path("C:/Users/Sam/AppData/Local/Temp/TODAY_CV.pdf")
    temp_ml = Path("C:/Users/Sam/AppData/Local/Temp/TODAY_Cover_Letter.pdf")
    shutil.copy2(pdf_file, temp_cv)
    if ml_pdf and ml_pdf.exists():
        shutil.copy2(ml_pdf, temp_ml)

    print(f"Staged CV to: {temp_cv}")
    print(f"Staged Cover Letter to: {temp_ml}")

if __name__ == "__main__":
    asyncio.run(main())
