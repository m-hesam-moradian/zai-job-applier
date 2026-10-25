import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import mm

temp_dir = Path(r"C:\Users\Sam\AppData\Local\Temp")
temp_dir.mkdir(parents=True, exist_ok=True)

output_dir = Path(r"F:\talentflow-ai\output\arconsis_4475778025")
output_dir.mkdir(parents=True, exist_ok=True)

# 1. GENERATE CV
cv_temp_path = temp_dir / "Sam_Moradian_CV.pdf"
cv_save_path = output_dir / "Sam_Moradian_CV.pdf"

styles = getSampleStyleSheet()

primary_color = colors.HexColor("#005A9C") # arconsis Deep Blue
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
    story.append(Paragraph("Senior Software Engineer AI & Cloud | AI@Scale & Resilient Cloud Architecture", title_style))
    contact_info = "Ardabil, Iran (EU Blue Card & Fast-Track § 81a AufenthG Eligible) | +1 805 900 7207 | m.hesam.moradian@gmail.com | linkedin.com/in/m-hesam-moradian | github.com/m-hesam-moradian"
    story.append(Paragraph(contact_info, contact_style))
    story.append(Spacer(1, 2*mm))
    story.append(HRFlowable(width="100%", thickness=0.75, color=primary_color, spaceAfter=4, spaceBefore=2))

    # Profile Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
    summary_text = (
        "Accomplished Senior AI & Cloud Software Engineer with 5+ years of experience engineering resilient, production-scale "
        "cloud-native applications and deploying AI@Scale pipelines. Expert in designing high-throughput Python and TypeScript "
        "backends, event-driven microservices, container orchestration (Docker), and multi-agent LLM systems (LangGraph, LiteLLM). "
        "Proven track record translating business strategy into robust software solutions. Completely aligned with arconsis's "
        "mission of bringing AI from experimentation into dependable production reality. Fully EU Blue Card eligible (§ 81a AufenthG)."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceAfter=4, spaceBefore=4))

    # Core Competencies
    story.append(Paragraph("CORE COMPETENCIES & TECHNICAL EXPERTISE", section_heading))
    skills = [
        "<b>AI@Scale & ML Engineering:</b> LangGraph, LiteLLM, LangChain, PyTorch, XGBoost, Scikit-learn, Multi-Agent Architecture, RAG",
        "<b>Cloud & Backend Development:</b> Python (FastAPI, Flask), TypeScript/JavaScript (Node.js, Express, React, Next.js), SQL",
        "<b>Cloud Infrastructure & DevOps:</b> Docker, Kubernetes, CI/CD (GitHub Actions), PostgreSQL, CouchDB, Redis, REST APIs, GraphQL",
        "<b>Software Engineering Excellence:</b> Clean Architecture, Event-Driven Systems, Automated E2E Testing (Playwright, Pytest), SSDLC"
    ]
    for sk in skills:
        story.append(Paragraph(f"• {sk}", bullet_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceAfter=4, spaceBefore=4))

    # Professional Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_heading))

    story.append(Paragraph("<b>The Million Project</b> | Senior Full-Stack & AI Cloud Engineer | 2024 – Present", bold_body))
    exp1 = [
        "Architected multi-agent LangGraph pipelines and LiteLLM model routing in production cloud environments, cutting API token costs by 40%.",
        "Built Next.js 14 + tRPC + PostgreSQL cloud application serving 10,000+ monthly active users with sub-200ms P95 latency.",
        "Engineered automated GitHub Actions CI/CD workflows and comprehensive test suites, achieving a 98% deployment success rate."
    ]
    for b in exp1:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("<b>Journal of Sustainable Energy Systems (JSES)</b> | Machine Learning & Deep Learning Engineer | 2023 – Present", bold_body))
    exp2 = [
        "Designed prescriptive energy modeling pipelines combining XGBoost, Elastic Net regression, and causal inference for grid forecasting.",
        "Published research integrating deep learning models (PyTorch) with evolutionary optimization algorithms for sustainable energy systems.",
        "Built automated data ingestion microservices with FastAPI, reducing preprocessing latency and operational overhead by 70%."
    ]
    for b in exp2:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("<b>Independent / Freelance</b> | Senior Software & Cloud Engineer | 2021 – 2024", bold_body))
    exp3 = [
        "Delivered 15+ production cloud applications and custom microservices for international clients across Europe and North America.",
        "Engineered secure JWT authentication services, RESTful APIs, and responsive web clients achieving 90+ Lighthouse scores."
    ]
    for b in exp3:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceAfter=4, spaceBefore=4))

    # Education & Immigration Status
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
cl_save_path = output_dir / "Sam_Moradian_Cover_Letter.pdf"

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
        "<b>arconsis IT-Solutions GmbH</b><br/>"
        "Talent Acquisition / Engineering Team<br/>"
        "Emmy-Noether-Straße 9<br/>"
        "76131 Karlsruhe, Germany<br/><br/>"
        "<b>Application for: Senior Software Engineer AI/Cloud (All genders) (Ref. 1986813)</b>"
    )
    story.append(Paragraph(recipient_info, body_style))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Dear Hiring Team at arconsis,", ParagraphStyle("Salutation", parent=body_style, fontName="Helvetica-Bold")))
    story.append(Spacer(1, 2*mm))

    p1 = (
        "I am writing to express my strong enthusiasm for the <b>Senior Software Engineer AI/Cloud (All genders)</b> position at "
        "arconsis IT-Solutions GmbH. With more than 5 years of hands-on experience designing scalable cloud-native architectures and "
        "deploying AI@Scale solutions, I share arconsis's dedication to moving artificial intelligence beyond simple experiments into "
        "dependable, production-ready enterprise systems that create lasting business value."
    )
    story.append(Paragraph(p1, body_style))
    story.append(Spacer(1, 2.5*mm))

    p2 = (
        "In my current position as Senior Full-Stack & AI Cloud Engineer at The Million Project, I design and operate multi-agent "
        "LangGraph systems integrated with LiteLLM routing and automated guardrails. By combining modern cloud microservices (FastAPI, "
        "PostgreSQL, Docker) with intelligent routing, I reduced inference latency and lowered API operational costs by 40%. Concurrently, "
        "at the Journal of Sustainable Energy Systems (JSES), I developed predictive and prescriptive pipelines with PyTorch, XGBoost, "
        "and Scikit-learn for complex energy optimization—work published in peer-reviewed scientific literature."
    )
    story.append(Paragraph(p2, body_style))
    story.append(Spacer(1, 2.5*mm))

    p3 = (
        "I value software craftsmanship, clean architecture, and practical engineering rigor. Whether designing cloud microservices, "
        "implementing robust CI/CD automation with GitHub Actions, or architecting multi-model AI workflows, my goal is always to deliver "
        "resilient software that scales smoothly."
    )
    story.append(Paragraph(p3, body_style))
    story.append(Spacer(1, 2.5*mm))

    p4 = (
        "My B.Sc. in Computer Engineering is recognized at German Grade 1.5 (Sehr Gut, Anabin H+), granting full qualification for the "
        "accelerated EU Blue Card under the Fast-Track Skilled Worker program (§ 81a AufenthG). I am ready to relocate to Karlsruhe or work "
        "across Germany immediately."
    )
    story.append(Paragraph(p4, body_style))
    story.append(Spacer(1, 2.5*mm))

    p5 = (
        "Thank you for considering my application. I look forward to the opportunity to speak with your team about how I can contribute "
        "to arconsis's AI@Scale and cloud engineering initiatives."
    )
    story.append(Paragraph(p5, body_style))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Sincerely,<br/><b>Sam Moradian</b>", body_style))

    doc.build(story)

build_cover_letter(cl_temp_path)
build_cover_letter(cl_save_path)
print(f"Cover letter built successfully: {cl_temp_path}")
