import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
from src.schemas.models import DynamicCandidateProfile
from src.tailor.cv_template import render_cv_html

async def main():
    profile_data = json.loads(Path("F:/talentflow-ai/data/ultimate_profile.json").read_text(encoding="utf-8"))
    profile = DynamicCandidateProfile.model_validate(profile_data)

    html = render_cv_html(profile)
    html_path = Path("F:/talentflow-ai/output/test_cv.html")
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html, encoding="utf-8")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({"width": 794, "height": 1123})
        await page.goto(html_path.as_uri(), wait_until="networkidle")

        pdf_path = Path("F:/talentflow-ai/output/Sam_Moradian_CV.pdf")
        await page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}
        )
        print("Generated PDF:", pdf_path, f"({pdf_path.stat().st_size} bytes)")

        # Render preview screenshot as PNG
        png_path = Path("F:/talentflow-ai/output/Sam_Moradian_CV_preview.png")
        await page.screenshot(path=str(png_path), full_page=False)
        print("Generated PNG preview:", png_path, f"({png_path.stat().st_size} bytes)")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
