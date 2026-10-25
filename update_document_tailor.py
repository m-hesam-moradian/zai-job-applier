from pathlib import Path

path = Path("F:/talentflow-ai/src/tailor/document_tailor.py")
content = path.read_text(encoding="utf-8")

split_mark = "def compile_application_pdfs("
prefix, _ = content.split(split_mark, 1)

new_code = '''def compile_application_pdfs(
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

    for para in package.motivation_letter.split("\\n\\n"):
        ml_story.append(Paragraph(para.replace("\\n", "<br/>"), letter_style))

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
'''

path.write_text(prefix + new_code, encoding="utf-8")
print("Successfully updated document_tailor.py")
