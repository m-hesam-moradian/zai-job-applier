import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

from src.schemas.models import DynamicCandidateProfile, JobPosting
from src.tailor.document_tailor import tailor_application_for_job
from src.tailor.cv_template import render_cv_html

async def main():
    profile_path = Path("F:/talentflow-ai/data/ultimate_profile.json")
    profile = DynamicCandidateProfile.model_validate(json.loads(profile_path.read_text(encoding="utf-8")))

    # Load Tappz job description
    with open("F:/talentflow-ai/JD-Datasets/linkedin_selected_jobs_2026-10-20.json", encoding="utf-8") as f:
        jobs = json.load(f)

    tappz_raw = next(j for j in jobs if str(j.get("jobId") or j.get("id")) == "4470109327")
    job = JobPosting(
        id="4470109327",
        title=tappz_raw.get("title", "Senior Fullstack Engineer (LLMs & AI Agents)"),
        company="Tappz GmbH",
        location=tappz_raw.get("location", "Munich, Bavaria, Germany"),
        description=tappz_raw.get("description", ""),
        url=tappz_raw.get("applyUrl") or tappz_raw.get("url", ""),
    )

    # Tailor package specifically for Tappz JD
    pkg = tailor_application_for_job(job, profile)
    print(f"Tailored for {job.company} - Match score: {pkg.match_score}%")
    print(f"Headline: {pkg.tailored_headline}")
    print(f"Top Skills: {', '.join(pkg.selected_skills[:10])}")

    # Generate HTML with ATS-optimized keywords matching JD
    html_content = render_cv_html(profile, pkg)

    out_dir = Path("F:/talentflow-ai/output/Tappz_GmbH_4470109327")
    out_dir.mkdir(parents=True, exist_ok=True)

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

    print(f"PDF generated: {pdf_file} ({pdf_file.stat().st_size} bytes)")
    print(f"PNG preview: {preview_png}")

if __name__ == "__main__":
    asyncio.run(main())
