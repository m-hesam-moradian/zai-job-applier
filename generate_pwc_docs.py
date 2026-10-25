import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import mm

temp_dir = Path(r"C:\Users\Sam\AppData\Local\Temp")
temp_dir.mkdir(parents=True, exist_ok=True)

pwc_dir = Path(r"F:\talentflow-ai\output\PwC_4472860977")
pwc_dir.mkdir(parents=True, exist_ok=True)

# 1. GENERATE CV
cv_temp_path = temp_dir / "Sam_Moradian_CV.pdf"
cv_save_path = pwc_dir / "Sam_Moradian_CV.pdf"

styles = getSampleStyleSheet()

primary_color = colors.HexColor("#D04A02") # PwC Orange / Amber
dark_text = colors.HexColor("#2D2D2D")
gray_text = colors.HexColor("#555555")
line_color = colors.HexColor("#E0E0E0")

name_style = ParagraphStyle(
    "Name",
    parent=styles["Heading1"],
    fontSize=20,
    leading=24,
    textColor=colors.HexColor("#1A1A1A"),
    spaceAfter=3,
    fontName="Helvetica-Bold"
)

title_style = ParagraphStyle(
    "Title",
    parent=styles["Normal"],
    fontSize=11,
    leading=14,
    textColor=primary_color,
    fontName="Helvetica-Bold",
    spaceAfter=4
)

contact_style = ParagraphStyle(
    "Contact",
    parent=styles["Normal"],
    fontSize=8.5,
    leading=12,
    textColor=gray_text,
    fontName="Helvetica"
)

section_heading = ParagraphStyle(
    "SectionHeading",
    parent=styles["Heading2"],
    fontSize=11,
    leading=14,
    textColor=colors.HexColor("#1A1A1A"),
    fontName="Helvetica-Bold",
    spaceBefore=7,
    spaceAfter=3
)

body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontSize=8.5,
    leading=12,
    textColor=dark_text,
    fontName="Helvetica",
    spaceAfter=2
)

bold_body = ParagraphStyle(
    "BoldBody",
    parent=body_style,
    fontName="Helvetica-Bold"
)

bullet_style = ParagraphStyle(
    "Bullet",
    parent=body_style,
    leftIndent=10,
    spaceAfter=1.5
)

def build_cv(filename):
    doc = SimpleDocTemplate(
        str(filename),
        pagesize=A4,
        leftMargin=14*mm,
        rightMargin=14*mm,
        topMargin=12*mm,
        bottomMargin=12*mm
    )
    story = []

    story.append(Paragraph("Sam Moradian", name_style))
    story.append(Paragraph("AI-Developer & Senior Full-Stack Engineer | Applied AI & Distributed Systems", title_style))
    contact_info = "Ardabil, Iran (EU Blue Card & Fast-Track § 81a AufenthG Eligible) | +1 805 900 7207 | m.hesam.moradian@gmail.com | linkedin.com/in/m-hesam-moradian | github.com/m-hesam-moradian"
    story.append(Paragraph(contact_info, contact_style))
    story.append(Spacer(1, 2*mm))
    story.append(HRFlowable(width="100%", thickness=0.75, color=primary_color, spaceAfter=4, spaceBefore=2))

    # Profile Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
    summary_text = (
        "Versatile Senior AI & Full-Stack Engineer with 5+ years of experience engineering resilient, production-grade "
        "AI microservices, multi-agent LLM systems (LangGraph, LiteLLM), and enterprise architectures. Deep background in "
        "Python, FastAPI, TypeScript, PyTorch, and cloud platforms. Proven track record architecting high-impact solutions "
        "and published machine learning research in energy demand forecasting. Completely aligned with PwC's technology and "
        "consulting excellence for Public Sector & Energy transformation."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceAfter=4, spaceBefore=4))

    # Core Competencies
    story.append(Paragraph("CORE COMPETENCIES & TECHNICAL EXPERTISE", section_heading))
    skills = [
        "<b>Languages & Frameworks:</b> Python (FastAPI, Flask, Django), TypeScript/JavaScript (Node.js, React, Next.js), SQL",
        "<b>AI & Machine Learning:</b> LangGraph, LiteLLM, LangChain, PyTorch, XGBoost, Scikit-learn, Multi-Agent Systems, RAG",
        "<b>Data & Cloud Infrastructure:</b> PostgreSQL, CouchDB, Redis, Docker, CI/CD (GitHub Actions), REST APIs, GraphQL",
        "<b>Domain Alignment:</b> Energy Systems Modeling, Public Sector Digitalization, Enterprise AI Architecture, Cloud Deployment"
    ]
    for sk in skills:
        story.append(Paragraph(f"• {sk}", bullet_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceAfter=4, spaceBefore=4))

    # Professional Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_heading))

    story.append(Paragraph("<b>The Million Project</b> | Senior Full-Stack & AI Engineer | 2024 – Present", bold_body))
    exp1 = [
        "Architected multi-agent LangGraph orchestration pipelines with LiteLLM routing across diverse foundation models, driving 40% reduction in API operating costs.",
        "Built enterprise Next.js + tRPC + PostgreSQL full-stack platforms serving 10,000+ active users with sub-200ms P95 latency.",
        "Engineered robust CI/CD workflows using GitHub Actions and automated Playwright E2E testing suites, achieving a 98% deployment success rate."
    ]
    for b in exp1:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("<b>Journal of Sustainable Energy Systems (JSES)</b> | Machine Learning & Deep Learning Engineer | 2023 – Present", bold_body))
    exp2 = [
        "Designed prescriptive energy modeling pipelines integrating XGBoost, Elastic Net, and causal inference for renewable demand forecasting.",
        "Authored peer-reviewed research combining PyTorch deep learning models with evolutionary optimization for sustainable energy grid reliability.",
        "Constructed automated data ingestion and validation pipelines, reducing data latency and processing overhead by 70%."
    ]
    for b in exp2:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("<b>Independent / Freelance</b> | Senior Software & AI Engineer | 2021 – 2024", bold_body))
    exp3 = [
        "Delivered 15+ production full-stack systems and custom automation workflows for international clients across Europe and North America.",
        "Implemented high-concurrency microservices, JWT authentication infrastructures, and seamless third-party enterprise integrations."
    ]
    for b in exp3:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceAfter=4, spaceBefore=4))

    # Education & Certifications
    story.append(Paragraph("EDUCATION & IMMIGRATION STATUS", section_heading))
    edu = [
        "<b>B.Sc. in Computer Engineering</b> | Islamic Azad University (German Grade Equivalent: 1.5 Sehr Gut, Anabin H+)",
        "<b>CS50x Introduction to Computer Science</b> | Harvard University (Verified Certificate)",
        "<b>Immigration Status:</b> Fast-Track Skilled Worker (§ 81a AufenthG) & EU Blue Card eligible; ready for immediate relocation to Germany."
    ]
    for e in edu:
        story.append(Paragraph(f"• {e}", bullet_style))

    doc.build(story)

build_cv(cv_temp_path)
build_cv(cv_save_path)
print(f"CV built successfully: {cv_temp_path}")

# 2. GENERATE MOTIVATION LETTER
cl_temp_path = temp_dir / "Sam_Moradian_Cover_Letter.pdf"
cl_save_path = pwc_dir / "Sam_Moradian_Cover_Letter.pdf"

def build_cover_letter(filename):
    doc = SimpleDocTemplate(
        str(filename),
        pagesize=A4,
        leftMargin=18*mm,
        rightMargin=18*mm,
        topMargin=16*mm,
        bottomMargin=16*mm
    )
    story = []

    story.append(Paragraph("Sam Moradian", name_style))
    story.append(Paragraph("Ardabil, Iran | +1 805 900 7207 | m.hesam.moradian@gmail.com | linkedin.com/in/m-hesam-moradian", contact_style))
    story.append(Spacer(1, 3*mm))
    story.append(HRFlowable(width="100%", thickness=0.75, color=primary_color, spaceAfter=6, spaceBefore=2))

    recipient_info = (
        "<b>PricewaterhouseCoopers GmbH Wirtschaftsprüfungsgesellschaft</b><br/>"
        "Recruiting Team – Public Sector & Energy<br/>"
        "Friedrich-Ebert-Anlage 35-37<br/>"
        "60327 Frankfurt am Main, Germany<br/><br/>"
        "<b>Application for: AI-Developer - Public Sector & Energy (w/m/d) (Ref. 2511)</b>"
    )
    story.append(Paragraph(recipient_info, body_style))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Dear Hiring Team at PwC Germany,", ParagraphStyle("Salutation", parent=body_style, fontName="Helvetica-Bold")))
    story.append(Spacer(1, 2*mm))

    p1 = (
        "I am writing to express my strong enthusiasm for the <b>AI-Developer - Public Sector & Energy (w/m/d)</b> "
        "position at PwC Germany. With over 5 years of specialized experience in architecting full-stack AI applications, "
        "multi-agent orchestration systems, and applied machine learning models for sustainable energy systems, I am excited to "
        "contribute directly to PwC's strategic initiatives in digitalizing the public sector and optimizing the energy transition."
    )
    story.append(Paragraph(p1, body_style))
    story.append(Spacer(1, 2.5*mm))

    p2 = (
        "In my current role as Senior Full-Stack & AI Engineer at The Million Project, I design and deploy multi-agent "
        "LangGraph pipelines integrated with LiteLLM routing and production FastAPI microservices, reducing LLM token costs "
        "by 40% while ensuring strict enterprise latency standards. Simultaneously, at the Journal of Sustainable Energy Systems "
        "(JSES), I have developed prescriptive analytics and predictive pipelines using PyTorch, XGBoost, and Scikit-learn for "
        "energy demand forecasting and grid optimization—research that has been published in peer-reviewed venues."
    )
    story.append(Paragraph(p2, body_style))
    story.append(Spacer(1, 2.5*mm))

    p3 = (
        "PwC's commitment to delivering trust and impactful technological transformation in the energy and public sector "
        "closely resonates with my professional journey. My academic degree in Computer Engineering is evaluated at German Grade 1.5 "
        "(Sehr Gut, Anabin H+), making me fully eligible for the accelerated EU Blue Card under the Fast-Track Skilled Worker program "
        "(§ 81a AufenthG). I am prepared to relocate to Germany immediately and bring full dedication, flexibility across office locations, "
        "and client-focused delivery."
    )
    story.append(Paragraph(p3, body_style))
    story.append(Spacer(1, 2.5*mm))

    p4 = (
        "Thank you very much for your time and consideration. I would welcome the opportunity to discuss in an interview how my "
        "hands-on AI engineering expertise can drive value for PwC and your clients in the public sector and energy industry."
    )
    story.append(Paragraph(p4, body_style))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Sincerely,<br/><b>Sam Moradian</b>", body_style))

    doc.build(story)

build_cover_letter(cl_temp_path)
build_cover_letter(cl_save_path)
print(f"Cover letter built successfully: {cl_temp_path}")
