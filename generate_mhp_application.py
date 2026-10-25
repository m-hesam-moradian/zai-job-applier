import asyncio
import json
import shutil
import sys
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

from src.schemas.models import DynamicCandidateProfile, JobPosting
from src.tailor.document_tailor import tailor_application_for_job, compile_application_pdfs
from src.tailor.cv_template import render_cv_html

async def main():
    profile_path = Path("F:/talentflow-ai/data/ultimate_profile.json")
    profile = DynamicCandidateProfile.model_validate(json.loads(profile_path.read_text(encoding="utf-8")))

    with open("F:/talentflow-ai/JD-Datasets/linkedin_selected_jobs_2026-10-24.json", encoding="utf-8") as f:
        jobs = json.load(f)

    job_raw = next(j for j in jobs if str(j.get("jobId") or j.get("id")) == "4482857863")
    job = JobPosting(
        id="4482857863",
        title="(Senior) Forward Deployed Technologist Cloud & Agentic AI (all genders)",
        company="MHP – A Porsche Company",
        location="Berlin / Nationwide, Germany (Hybrid)",
        description=job_raw.get("description", ""),
        url=job_raw.get("applyUrl") or job_raw.get("url", ""),
    )

    pkg = tailor_application_for_job(job, profile)
    print(f"Tailored for {job.company} - Match score: {pkg.match_score}%")
    print(f"Headline: {pkg.tailored_headline}")
    print(f"Top Skills: {', '.join(pkg.selected_skills[:10])}")

    out_dir = Path("F:/talentflow-ai/output/MHP_Porsche_4482857863")
    out_dir.mkdir(parents=True, exist_ok=True)

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

    pdf_paths = compile_application_pdfs(pkg, profile, Path("F:/talentflow-ai/output"))
    print(f"PDFs compiled: {pdf_paths}")

    # Stage files strictly under candidate personal name (NEVER company name)
    temp_cv = Path("C:/Users/Sam/AppData/Local/Temp/Sam_Moradian_CV.pdf")
    shutil.copyfile(pdf_file, temp_cv)
    print(f"Staged CV to {temp_cv}")

    txt_path = out_dir / "Sam_Moradian_Cover_Letter.txt"
    txt_path.write_text(pkg.motivation_letter, encoding="utf-8")
    print(f"Saved cover letter text: {txt_path}")

    mot_src = pdf_paths.get("motivation_pdf")
    temp_mot = Path("C:/Users/Sam/AppData/Local/Temp/Sam_Moradian_Cover_Letter.pdf")
    if mot_src and Path(mot_src).exists():
        shutil.copyfile(mot_src, temp_mot)
        print(f"Staged cover letter to {temp_mot}")

if __name__ == "__main__":
    asyncio.run(main())
