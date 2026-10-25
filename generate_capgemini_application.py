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

    job_raw = next(j for j in jobs if str(j.get("jobId") or j.get("id")) == "4398263346")
    job = JobPosting(
        id="4398263346",
        title="(Senior) Manager AI Systems & Platform Architecture/Developer (w/m/d)",
        company="Capgemini Invent",
        location="Stuttgart / Berlin / Munich, Germany (Hybrid)",
        description=job_raw.get("description", ""),
        url=job_raw.get("applyUrl") or job_raw.get("url", ""),
    )

    pkg = tailor_application_for_job(job, profile)
    print(f"Tailored for {job.company} - Match score: {pkg.match_score}%")
    print(f"Headline: {pkg.tailored_headline}")
    print(f"Top Skills: {', '.join(pkg.selected_skills[:10])}")

    out_dir = Path("F:/talentflow-ai/output/Capgemini_Invent_4398263346")
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

    temp_cv = Path("C:/Users/Sam/AppData/Local/Temp/Capgemini_CV.pdf")
    shutil.copyfile(pdf_file, temp_cv)
    print(f"Staged CV to {temp_cv}")

    txt_path = out_dir / "Sam_Moradian_Motivation_Letter.txt"
    txt_path.write_text(pkg.motivation_letter, encoding="utf-8")
    print(f"Saved motivation letter text: {txt_path}")

    mot_src = pdf_paths.get("motivation_pdf")
    if mot_src and Path(mot_src).exists():
        temp_mot = Path("C:/Users/Sam/AppData/Local/Temp/Capgemini_Motivation_Letter.pdf")
        shutil.copyfile(mot_src, temp_mot)
        print(f"Staged motivation letter to {temp_mot}")

    # Generate Academic Credentials and Reference Summary PDF
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

    cred_pdf = out_dir / "Sam_Moradian_Academic_and_Reference_Credentials.pdf"
    doc = SimpleDocTemplate(str(cred_pdf), pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm)
    styles = getSampleStyleSheet()

    story = [
        Paragraph("<b>ACADEMIC CREDENTIALS &amp; PROFESSIONAL REFERENCES</b>", ParagraphStyle('Title', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor('#0070ad'))),
        Paragraph("<b>Sam Moradian</b> | m.hesam.moradian@gmail.com | +18059007207", ParagraphStyle('Sub', parent=styles['Normal'], fontSize=9, leading=12, textColor=colors.HexColor('#555555'))),
        Spacer(1, 3*mm),
        HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#0070ad')),
        Spacer(1, 4*mm),
        Paragraph("<b>1. HIGHER EDUCATION &amp; DEGREE RECOGNITION</b>", ParagraphStyle('H2', parent=styles['Heading2'], fontSize=11, leading=14, textColor=colors.HexColor('#111111'))),
        Paragraph("• <b>Bachelor of Science in Computer Engineering</b> — Islamic Azad University (IAU)", ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=13)),
        Paragraph("  - German Grade Equivalence: <b>1.5 ('Sehr Gut')</b>", ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=13)),
        Paragraph("  - German Anabin Status: <b>H+ Institution Recognized</b> (fulfills statutory criteria for Section 81a AufenthG Accelerated Skilled Worker Procedure and EU Blue Card)", ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=13)),
        Spacer(1, 3*mm),
        Paragraph("• <b>CS50x: Introduction to Computer Science</b> — Harvard University / edX", ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=13)),
        Paragraph("  - Verification ID: Certified Honors Graduate | Intensive software architecture &amp; algorithms", ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=13)),
        Spacer(1, 4*mm),
        Paragraph("<b>2. EMPLOYMENT ANCHORS &amp; PROFESSIONAL REFERENCES</b>", ParagraphStyle('H2', parent=styles['Heading2'], fontSize=11, leading=14, textColor=colors.HexColor('#111111'))),
        Paragraph("• <b>The Million Project</b> — Senior Full-Stack Engineer (2024 – Present)", ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=13)),
        Paragraph("  - Core Impact: Multi-agent LangGraph pipelines, LiteLLM routing, and high-throughput production Next.js/tRPC infrastructure.", ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=13)),
        Paragraph("  - Reference Contact: Available upon formal interview request.", ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=13)),
        Spacer(1, 2*mm),
        Paragraph("• <b>Journal of Sustainable Energy Systems (JSES)</b> — Machine Learning &amp; Deep Learning Engineer (2023 – Present)", ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=13)),
        Paragraph("  - Core Impact: Prescriptive analytics, causal inference, and published peer-reviewed AI demand forecasting research.", ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=13)),
        Spacer(1, 2*mm),
        Paragraph("• <b>Independent Engineering Engagements</b> — Full-Stack &amp; AI Engineer (2021 – 2024)", ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=13)),
        Paragraph("  - Core Impact: Delivered 15+ full-stack production platforms with international client satisfaction.", ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=13)),
        Spacer(1, 4*mm),
        Paragraph("<b>3. WORK AUTHORIZATION &amp; RELOCATION READINESS</b>", ParagraphStyle('H2', parent=styles['Heading2'], fontSize=11, leading=14, textColor=colors.HexColor('#111111'))),
        Paragraph("• Full statutory eligibility for the <b>EU Blue Card (Blaue Karte EU)</b> and German Accelerated Skilled Worker Procedure (<b>§ 81a AufenthG</b>). Immediate availability upon contract offer.", ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=13)),
    ]
    doc.build(story)
    print(f"Generated credentials reference PDF: {cred_pdf}")

    temp_cred = Path("C:/Users/Sam/AppData/Local/Temp/Capgemini_References.pdf")
    shutil.copyfile(cred_pdf, temp_cred)
    print(f"Staged credentials to {temp_cred}")

if __name__ == "__main__":
    asyncio.run(main())
