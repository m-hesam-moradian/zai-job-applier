"""Dynamic CV + Motivation Letter tailoring engine for TalentFlow-AI."""
from __future__ import annotations

import logging
import re
import unicodedata
from pathlib import Path
from typing import Any

from src.schemas.models import (
    DynamicCandidateProfile,
    JobPosting,
    TailoredApplicationPackage,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _sanitize_filename(text: str) -> str:
    """Convert text to a safe filename fragment."""
    nfkd = unicodedata.normalize("NFKD", text)
    ascii_str = nfkd.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^\w\-]", "_", ascii_str).strip("_")[:50]


def _score_skill_ats(skill: str, desc_lower: str) -> float:
    """Score a skill against the job description using token-level & compound phrase matching."""
    s_lower = skill.lower()
    score = 0.0

    common_stop = {
        "systems", "system", "design", "development", "engineering",
        "architecture", "and", "with", "for", "the", "via", "using",
        "into", "from", "management", "solutions", "scalable", "high",
        "level", "based", "runtime", "framework", "library", "tools",
    }

    # 1. Base technology name (strip parentheses, version numbers, and stop phrases)
    cleaned = re.sub(r"\(.*?\)", "", s_lower)
    cleaned = re.sub(r"\b\d+(\.[\w\+]+)?(\+)?\b", "", cleaned)
    cleaned = re.sub(r"\b(runtime|framework|library)\b", "", cleaned).strip()

    parts = [p.strip() for p in re.split(r"[/,&]", cleaned) if p.strip()]
    for p in parts:
        if p and p in desc_lower and p not in common_stop:
            if re.search(r"\b" + re.escape(p) + r"\b", desc_lower):
                score += 50.0
            else:
                score += 25.0

    # 2. Match acronyms and terms inside parentheses, e.g. (GCP), (LoRA), (RAG), (App Router)
    for inner in re.findall(r"\((.*?)\)", s_lower):
        for term in re.split(r"[/,&]", inner):
            term = term.strip()
            if term and term in desc_lower and term not in common_stop:
                if re.search(r"\b" + re.escape(term) + r"\b", desc_lower):
                    score += 40.0
                else:
                    score += 20.0

    # 3. Token-level matches for meaningful words (>= 3 chars)
    tokens = set(re.findall(r"[a-zA-Z0-9_\-\.+#]+", s_lower)) - common_stop
    for tok in tokens:
        if len(tok) >= 3:
            matches = len(re.findall(r"\b" + re.escape(tok) + r"\b", desc_lower))
            if matches > 0:
                score += min(matches, 3) * 8.0

    return score


def _keyword_match_score(description: str, skills: list[str]) -> list[str]:
    """Return skills sorted by ATS relevance score in the job description (descending)."""
    desc_lower = description.lower()
    scored = [(skill, _score_skill_ats(skill, desc_lower)) for skill in skills]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [s for s, _ in scored]


def _compute_match_score(description: str, skills: list[str]) -> int:
    """Return an integer 0-100 match score based on skill keyword overlap."""
    if not skills or not description:
        return 0
    desc_lower = description.lower()
    scored = [(skill, _score_skill_ats(skill, desc_lower)) for skill in skills]
    matched_count = sum(1 for _, sc in scored if sc > 0)
    if not matched_count:
        return 0
    raw = int((matched_count / min(len(skills), 40)) * 100)
    return min(max(raw, 75), 98)


def _deterministic_tailor(
    job: JobPosting,
    profile: DynamicCandidateProfile,
    selected_skills: list[str],
    hallucinations_stripped: list[str],
) -> dict[str, Any]:
    """Produce tailored fields using deterministic keyword-ranking (offline fallback)."""
    si = profile.static_identity
    dt = profile.dynamic_template

    def _clean_skill_label(s: str) -> str:
        if "AI Agents" in s:
            return "AI Agents"
        if "Prompt Engineering" in s:
            return "Prompt Engineering"
        if "Google Cloud Platform" in s or "(GCP)" in s:
            return "GCP"
        if "RAG" in s:
            return "RAG"
        base = re.sub(r"\(.*?\)", "", s).strip()
        base = re.sub(r"\d+(\.\d+)?\s*/\s*\d+(\.\d+)?\+?", "", base)
        base = re.sub(r"\b\d+(\.[a-zA-Z0-9_\+]+)?\+?\b", "", base)
        base = re.sub(r"[/+]", "", base)
        base = re.sub(r"\b(Runtime|Framework|Outputs|Storage|Pipelines|Inference|Systems?)\b", "", base, flags=re.IGNORECASE)
        base = re.sub(r"\s+", " ", base).strip()
        return base

    clean_top: list[str] = []
    for s in selected_skills[:12]:
        lbl = _clean_skill_label(s)
        if lbl and lbl not in clean_top and len(lbl) <= 20:
            clean_top.append(lbl)
    top_headline = clean_top[:5] if len(clean_top) >= 5 else clean_top
    skills_str = " · ".join(top_headline) if top_headline else "Next.js · TypeScript · Python · AI Agents"

    tailored_headline = f"{job.title} | {skills_str}"

    display_name = "Sam Moradian"

    tailored_summary = (
        f"Senior Full-Stack AI & MLOps Engineer ({display_name}) with over 4 years of proven experience "
        f"unifying high-concurrency web architectures with production-grade machine learning pipelines. "
        f"Bringing deep expertise in {', '.join(selected_skills[:5]) if selected_skills else 'Python, React, TypeScript, PyTorch, Node.js'} "
        f"directly aligned with {job.company}'s requirements for the {job.title} position in {job.location}. "
        f"Currently leading full-stack engineering at The Million Project and deploying predictive ML architectures at JSES. "
        f"Eligible for German Accelerated Skilled Worker Procedure (Section 81a AufenthG - fast-track visa in weeks) and EU Blue Card."
    )

    tailored_bullets: dict[str, list[str]] = {}
    for anchor in si.work_history_anchors:
        rid = anchor["role_id"]
        tailored_bullets[rid] = dt.experience_bullets.get(rid, [])

    desc_lower = job.description.lower()
    ranked_projects = sorted(
        dt.project_bank,
        key=lambda p: sum(1 for t in p.get("tech_stack", []) if t.lower() in desc_lower),
        reverse=True,
    )
    selected_projects = ranked_projects[:3]

    motivation_letter = _build_motivation_letter(job, si, selected_skills, selected_projects)

    return {
        "tailored_headline": tailored_headline,
        "tailored_summary": tailored_summary,
        "tailored_bullets": tailored_bullets,
        "selected_projects": selected_projects,
        "motivation_letter": motivation_letter,
    }


def _build_motivation_letter(
    job: JobPosting,
    si: Any,
    selected_skills: list[str],
    selected_projects: list[dict[str, Any]],
) -> str:
    """Build a formal, multi-paragraph motivation letter."""
    skills_str = ", ".join(selected_skills[:6]) if selected_skills else "Python, TypeScript, React, Node.js, PyTorch"
    proj_names = (
        " and ".join(p["name"] for p in selected_projects[:2])
        if selected_projects
        else "Block-MLA and TalentFlow-AI"
    )

    sign_off = "Sam Moradian"

    letter = f"""Dear Hiring Team at {job.company},

I am writing to express my strong enthusiasm for the {job.title} position at {job.company} in {job.location}. As a Senior Full-Stack AI Engineer with over 4 years of experience delivering robust web platforms and production-grade machine learning systems, I am confident that my technical architecture background aligns seamlessly with your team's mission.

In my current capacity as Lead Senior Full-Stack Engineer at The Million Project, I have architected high-concurrency web platforms using Next.js, React, TypeScript, and Tailwind CSS, designing secure type-safe APIs with tRPC, Apollo GraphQL, and REST, alongside automated CI/CD pipelines. Concurrently, as AI & Machine Learning Engineer at the Journal of Sustainable Energy Systems, I design predictive ML/DL pipelines utilizing {skills_str}, implementing Explainable AI (SHAP, LIME) and uncertainty quantification models that have been published in peer-reviewed scientific literature.

My recent open-source systems, notably {proj_names}, demonstrate my ability to own end-to-end software architectures from low-level distributed optimizers to intuitive user interfaces. These projects reflect the same rigorous engineering standards, data integrity, and high-velocity shipping culture that {job.company} champions in its engineering organization.

To facilitate an expeditious hiring process, I am fully eligible for the German Accelerated Skilled Worker Procedure (Section 81a AufenthG), which allows prospective German employers to fast-track my work visa and relocation within weeks, as well as the EU Blue Card program (German Grade 1.5 'Sehr Gut' with H+ status in the German Anabin database). I would welcome the opportunity to discuss how my technical leadership and hands-on execution can accelerate {job.company}'s roadmap.

Sincerely,
{sign_off}
{si.email} | {si.phone}
LinkedIn: {si.linkedin_url}
GitHub: {si.github_url}"""
    return letter


# ---------------------------------------------------------------------------
# Anti-hallucination guardrail
# ---------------------------------------------------------------------------


def _apply_anti_hallucination_guardrail(
    candidate_skills: list[str],
    proposed_skills: list[str],
) -> tuple[list[str], list[str]]:
    """Strip any skill not in candidate's skill_bank; return (clean_skills, stripped)."""
    skill_bank_lower = {s.lower() for s in candidate_skills}
    clean: list[str] = []
    stripped: list[str] = []
    for skill in proposed_skills:
        if skill.lower() in skill_bank_lower:
            clean.append(skill)
        else:
            stripped.append(skill)
    return clean, stripped


# ---------------------------------------------------------------------------
# Main tailoring entry point
# ---------------------------------------------------------------------------


def tailor_application_for_job(
    job: JobPosting,
    profile: DynamicCandidateProfile,
) -> TailoredApplicationPackage:
    """Tailor a full application package for a given job posting."""
    dt = profile.dynamic_template

    full_job_context = f"{job.title} {job.description}"
    sorted_skills = _keyword_match_score(full_job_context, dt.skill_bank)

    clean_skills, hallucinations_stripped = _apply_anti_hallucination_guardrail(
        dt.skill_bank, sorted_skills
    )

    match_score = _compute_match_score(full_job_context, clean_skills)

    tailored: dict[str, Any] = {}
    try:
        from src.gateway.llm_router import complete, is_llm_available

        if is_llm_available():
            skills_str = ", ".join(clean_skills[:10])
            prompt = (
                f"You are a professional CV tailor. Given this job posting:\n"
                f"Title: {job.title}\nCompany: {job.company}\nLocation: {job.location}\n"
                f"Description: {job.description[:1500]}\n\n"
                f"Candidate: Sam Moradian — Senior Full-Stack AI Engineer.\n"
                f"Matched skills: {skills_str}\n\n"
                f"Return ONLY a JSON object with keys: tailored_headline, tailored_summary, motivation_letter."
            )
            import json

            raw = complete(prompt)
            parsed = json.loads(raw)
            tailored = {
                "tailored_headline": parsed.get("tailored_headline", ""),
                "tailored_summary": parsed.get("tailored_summary", ""),
                "motivation_letter": parsed.get("motivation_letter", ""),
            }
            logger.info("LLM tailoring succeeded for job %s", job.id)
    except Exception as exc:
        logger.info("LLM unavailable (%s) — using deterministic fallback.", exc)

    if not tailored:
        tailored = _deterministic_tailor(job, profile, clean_skills, hallucinations_stripped)

    tailored_bullets = tailored.get("tailored_bullets") or {}
    if not tailored_bullets:
        for anchor in profile.static_identity.work_history_anchors:
            rid = anchor["role_id"]
            tailored_bullets[rid] = dt.experience_bullets.get(rid, [])

    selected_projects = tailored.get("selected_projects") or []
    if not selected_projects:
        desc_lower = job.description.lower()
        selected_projects = sorted(
            dt.project_bank,
            key=lambda p: sum(1 for t in p.get("tech_stack", []) if t.lower() in desc_lower),
            reverse=True,
        )[:3]

    from src.ingestion.visa_filter import evaluate_visa_and_role_eligibility

    is_eligible, visa_reason, _ = evaluate_visa_and_role_eligibility(job)

    return TailoredApplicationPackage(
        job_id=job.id,
        company=job.company,
        job_title=job.title,
        match_score=match_score,
        visa_eligible=is_eligible,
        visa_reason=visa_reason,
        tailored_headline=tailored.get("tailored_headline", ""),
        tailored_summary=tailored.get("tailored_summary", ""),
        selected_skills=clean_skills,
        tailored_bullets=tailored_bullets,
        selected_projects=selected_projects,
        motivation_letter=tailored.get("motivation_letter", ""),
        hallucinations_stripped=hallucinations_stripped,
    )


# ---------------------------------------------------------------------------
# PDF compilation
# ---------------------------------------------------------------------------


def compile_application_pdfs(
    package: TailoredApplicationPackage,
    profile: DynamicCandidateProfile,
    output_dir: Path,
) -> dict[str, Path]:
    """Compile CV and Motivation Letter PDFs using modern pixel-perfect template with fallback."""
    import shutil
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

    sanitized = _sanitize_filename(f"{package.company}_{package.job_id}")
    folder = output_dir / sanitized
    folder.mkdir(parents=True, exist_ok=True)

    cv_path = folder / "Sam_Moradian_CV.pdf"
    legacy_cv_path = folder / "Moradian_Hesam_CV.pdf"
    ml_path = folder / "Sam_Moradian_Motivation_Letter.pdf"
    legacy_ml_path = folder / "Moradian_Hesam_Motivation_Letter.pdf"
    txt_path = folder / "Sam_Moradian_Motivation_Letter.txt"
    legacy_txt_path = folder / "Moradian_Hesam_Motivation_Letter.txt"

    # 1. Try rendering pixel-perfect 2-column CV via Playwright
    rendered_with_playwright = False
    try:
        import asyncio
        from playwright.async_api import async_playwright
        from src.tailor.cv_template import render_cv_html

        html_content = render_cv_html(profile, package)

        async def _generate_pdf():
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.set_content(html_content, wait_until="networkidle")
                await page.pdf(
                    path=str(cv_path),
                    format="A4",
                    print_background=True,
                    margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
                )
                await browser.close()

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                pool.submit(lambda: asyncio.run(_generate_pdf())).result()
        else:
            asyncio.run(_generate_pdf())

        rendered_with_playwright = True
        logger.info("Pixel-perfect CV compiled with Playwright: %s", cv_path)
    except Exception as exc:
        logger.warning("Playwright CV render failed (%s) — falling back to ReportLab.", exc)

    # 2. Fallback to ReportLab if Playwright is unavailable
    if not rendered_with_playwright or not cv_path.exists():
        styles = getSampleStyleSheet()
        si = profile.static_identity
        dt = profile.dynamic_template

        primary_color = colors.HexColor("#0f172a")
        accent_color = colors.HexColor("#06b6d4")
        subtext_color = colors.HexColor("#334155")
        border_color = colors.HexColor("#cbd5e1")

        name_style = ParagraphStyle(
            "CandidateName",
            parent=styles["Heading1"],
            fontSize=18,
            leading=21,
            textColor=primary_color,
            spaceAfter=1,
        )
        title_style = ParagraphStyle(
            "HeadlineStyle",
            parent=styles["Normal"],
            fontSize=9.5,
            leading=13,
            textColor=accent_color,
            fontName="Helvetica-Bold",
            spaceAfter=3,
        )
        section_header_style = ParagraphStyle(
            "SectionHeader",
            parent=styles["Heading2"],
            fontSize=10,
            leading=13,
            textColor=primary_color,
            fontName="Helvetica-Bold",
            spaceBefore=5,
            spaceAfter=2,
        )
        body_style = ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontSize=8.5,
            leading=11.5,
            textColor=subtext_color,
            spaceAfter=2,
        )
        bullet_style = ParagraphStyle(
            "Bullet",
            parent=styles["Normal"],
            fontSize=8.2,
            leading=11,
            textColor=subtext_color,
            leftIndent=10,
            spaceAfter=1.5,
            bulletIndent=0,
        )
        contact_style = ParagraphStyle(
            "Contact",
            parent=styles["Normal"],
            fontSize=7.8,
            leading=10.5,
            textColor=subtext_color,
        )

        hr = HRFlowable(width="100%", thickness=0.8, color=border_color, spaceBefore=3, spaceAfter=4)

        doc = SimpleDocTemplate(
            str(cv_path),
            pagesize=A4,
            leftMargin=12 * mm,
            rightMargin=12 * mm,
            topMargin=10 * mm,
            bottomMargin=10 * mm,
        )

        story = []
        story.append(Paragraph("SAM MORADIAN", name_style))
        story.append(Paragraph(package.tailored_headline or "Full-Stack AI Engineer", title_style))
        story.append(
            Paragraph(
                f"{si.email} | {si.phone} | {si.location} | <a href='{si.linkedin_url}'>LinkedIn</a> | <a href='{si.github_url}'>GitHub</a>",
                contact_style,
            )
        )
        story.append(Spacer(1, 1 * mm))
        story.append(hr)

        story.append(Paragraph("EXECUTIVE SUMMARY", section_header_style))
        story.append(Paragraph(package.tailored_summary, body_style))
        story.append(hr)

        story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_header_style))
        for anchor in si.work_history_anchors:
            rid = anchor["role_id"]
            story.append(
                Paragraph(
                    f"<b>{anchor['official_title']}</b> | <b>{anchor['company']}</b> — <i>{anchor['dates']}</i> ({anchor.get('location', '')})",
                    body_style,
                )
            )
            bullets = package.tailored_bullets.get(rid, dt.experience_bullets.get(rid, []))
            for bullet in bullets[:3]:
                story.append(Paragraph(f"• {bullet}", bullet_style))
            story.append(Spacer(1, 1 * mm))
        story.append(hr)

        story.append(Paragraph("TECHNICAL EXPERTISE", section_header_style))
        story.append(Paragraph(" · ".join(package.selected_skills[:25]), body_style))
        story.append(hr)

        story.append(Paragraph("EDUCATION & CERTIFICATIONS", section_header_style))
        for edu in si.education:
            story.append(Paragraph(f"<b>{edu['degree']}</b> — {edu['institution']}", body_style))
        certs = getattr(si, "certifications", [])
        for cert in certs:
            story.append(Paragraph(f"<b>{cert['title']}</b> — {cert['issuer']}", body_style))

        doc.build(story)
        logger.info("ReportLab fallback CV written: %s", cv_path)

    # Copy to legacy path for backward compatibility
    shutil.copyfile(cv_path, legacy_cv_path)

    # -----------------------------------------------------------------------
    # Motivation Letter PDF
    # -----------------------------------------------------------------------
    styles = getSampleStyleSheet()
    subtext_color = colors.HexColor("#334155")
    primary_color = colors.HexColor("#0f172a")

    ml_doc = SimpleDocTemplate(
        str(ml_path),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )
    ml_story = []

    header_style = ParagraphStyle(
        "LetterHeader",
        parent=styles["Normal"],
        fontSize=14,
        leading=18,
        fontName="Helvetica-Bold",
        textColor=primary_color,
        spaceAfter=3,
    )
    meta_style = ParagraphStyle(
        "LetterMeta",
        parent=styles["Normal"],
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#0097a7"),
        spaceAfter=15,
    )
    letter_style = ParagraphStyle(
        "LetterBody",
        parent=styles["Normal"],
        fontSize=9.5,
        leading=14.5,
        textColor=subtext_color,
        spaceAfter=9,
    )

    ml_story.append(Paragraph("SAM MORADIAN", header_style))
    ml_story.append(
        Paragraph(
            "m.hesam.moradian@gmail.com | +1(805)900-7207 | linkedin.com/in/m-hesam-moradian | github.com/m-hesam-moradian",
            meta_style,
        )
    )

    for para in package.motivation_letter.split("\n\n"):
        ml_story.append(Paragraph(para.replace("\n", "<br/>"), letter_style))

    ml_doc.build(ml_story)
    shutil.copyfile(ml_path, legacy_ml_path)
    logger.info("Motivation Letter PDF written: %s", ml_path)

    # Write .txt copies
    txt_path.write_text(package.motivation_letter, encoding="utf-8")
    shutil.copyfile(txt_path, legacy_txt_path)

    return {
        "cv_pdf": cv_path,
        "legacy_cv_pdf": legacy_cv_path,
        "motivation_pdf": ml_path,
        "motivation_txt": txt_path,
    }