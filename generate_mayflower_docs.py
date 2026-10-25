import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import mm

temp_dir = Path(r"C:\Users\Sam\AppData\Local\Temp")
temp_dir.mkdir(parents=True, exist_ok=True)

output_dir = Path(r"F:\talentflow-ai\output\Mayflower_4475189366")
output_dir.mkdir(parents=True, exist_ok=True)

# 1. GENERATE CV
cv_temp_path = temp_dir / "Sam_Moradian_CV.pdf"
cv_save_path = output_dir / "Sam_Moradian_CV.pdf"

styles = getSampleStyleSheet()

primary_color = colors.HexColor("#008080") # Teal / Emerald
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
    story.append(Paragraph("Senior AI Solutions Developer | Generative AI & Scalable Microservices", title_style))
    contact_info = "Ardabil, Iran (EU Blue Card & Fast-Track § 81a AufenthG Eligible) | +1 805 900 7207 | m.hesam.moradian@gmail.com | linkedin.com/in/m-hesam-moradian | github.com/m-hesam-moradian"
    story.append(Paragraph(contact_info, contact_style))
    story.append(Spacer(1, 2*mm))
    story.append(HRFlowable(width="100%", thickness=0.75, color=primary_color, spaceAfter=4, spaceBefore=2))

    # Profile Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
    summary_text = (
        "Pragmatic Senior AI Solutions Developer with 5+ years of experience engineering custom Generative AI applications, "
        "production multi-agent systems (LangGraph, LiteLLM), and enterprise full-stack web platforms. Proven expertise combining "
        "Python (FastAPI), TypeScript (React, Next.js), and containerized microservices (Docker) to deliver agile software "
        "that creates tangible customer value. Published machine learning researcher with peer-reviewed work in sustainable energy "
        "forecasting. Fully eligible for the accelerated EU Blue Card under the Fast-Track Skilled Worker program (§ 81a AufenthG)."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceAfter=4, spaceBefore=4))

    # Core Competencies
    story.append(Paragraph("CORE COMPETENCIES & TECHNICAL EXPERTISE", section_heading))
    skills = [
        "<b>Generative AI & Agentic Systems:</b> LangGraph, LiteLLM, LangChain, PyTorch, Multi-Agent Orchestration, RAG, Token Optimization",
        "<b>Full-Stack & Backend Engineering:</b> Python (FastAPI, Flask), TypeScript/JavaScript (Node.js, Express, React, Next.js), PostgreSQL",
        "<b>DevOps & Agile Delivery:</b> Docker, GitHub Actions CI/CD, Redis, CouchDB, RESTful APIs, GraphQL, TDD (Pytest, Playwright)",
        "<b>Consulting & Client Focus:</b> Agile Solution Engineering, Technical Sparring, Knowledge Sharing, Clean Code Architecture"
    ]
    for sk in skills:
        story.append(Paragraph(f"• {sk}", bullet_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceAfter=4, spaceBefore=4))

    # Professional Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_heading))

    story.append(Paragraph("<b>The Million Project</b> | Senior Full-Stack & AI Solutions Developer | 2024 – Present", bold_body))
    exp1 = [
        "Architected multi-agent LangGraph pipelines with dynamic LiteLLM routing across diverse model providers, cutting API costs by 40%.",
        "Built Next.js 14 + tRPC + PostgreSQL cloud application serving 10,000+ monthly active users with sub-200ms P95 latency.",
        "Engineered automated GitHub Actions CI/CD workflows and comprehensive test suites, achieving a 98% deployment success rate."
    ]
    for b in exp1:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("<b>Journal of Sustainable Energy Systems (JSES)</b> | Machine Learning & Deep Learning Engineer | 2023 – Present", bold_body))
    exp2 = [
        "Designed prescriptive energy modeling pipelines integrating XGBoost, Elastic Net regression, and causal inference for grid forecasting.",
        "Published research integrating deep learning models (PyTorch) with evolutionary optimization algorithms for sustainable energy systems.",
        "Constructed automated data validation microservices with FastAPI, reducing preprocessing latency and operational overhead by 70%."
    ]
    for b in exp2:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("<b>Independent / Freelance</b> | Senior Software & AI Engineer | 2021 – 2024", bold_body))
    exp3 = [
        "Delivered 15+ production applications and custom AI tools for international clients across Europe and North America.",
        "Built high-performance web clients with Tailwind CSS achieving Lighthouse scores of 90+."
    ]
    for b in exp3:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceAfter=4, spaceBefore=4))

    # Education & Immigration Status
    story.append(Paragraph("EDUCATION & IMMIGRATION STATUS", section_heading))
    edu = [
        "<b>B.Sc. in Computer Engineering</b> | Islamic Azad University (German Grade Equivalent: 1.5 Sehr Gut, Anabin H+)",
        "<b>CS50x Introduction to Computer Science</b> | Harvard University (Verified Certificate)",
        "<b>Immigration Status:</b> Fast-Track Skilled Worker (§ 81a AufenthG) & EU Blue Card eligible; ready for immediate relocation to Munich/Germany."
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
    story.append(Paragraph("Ardabil, Iran | +1 805 900 7207 | m.hesam.moradian@gmail.com | linkedin.com/in/m-hesam-moradian | github.com/m-hesam-moradian", contact_style))
    story.append(Spacer(1, 3*mm))
    story.append(HRFlowable(width="100%", thickness=0.75, color=primary_color, spaceAfter=6, spaceBefore=2))

    recipient_info = (
        "<b>Mayflower GmbH</b><br/>"
        "People & Organization / Recruiting Team<br/>"
        "Mannhardtstraße 6<br/>"
        "80538 Munich, Germany<br/><br/>"
        "<b>Application for: Senior AI Solutions Entwickler:in / Developer (Ref. 2290349)</b>"
    )
    story.append(Paragraph(recipient_info, body_style))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Dear Hiring Team at Mayflower GmbH,", ParagraphStyle("Salutation", parent=body_style, fontName="Helvetica-Bold")))
    story.append(Spacer(1, 2*mm))

    p1 = (
        "I am writing to express my strong interest in the <b>Senior AI Solutions Developer</b> position at Mayflower GmbH. "
        "As an experienced software engineer specialized in Generative AI, multi-agent frameworks, and modern full-stack development, "
        "Mayflower's established focus on custom software development, agile methodologies, and Generative AI solutions closely aligns "
        "with my technical passion and engineering values."
    )
    story.append(Paragraph(p1, body_style))
    story.append(Spacer(1, 2.5*mm))

    p2 = (
        "In my current role at The Million Project, I build and orchestrate multi-agent LangGraph architectures routed via LiteLLM "
        "across diverse foundation models. Through thoughtful prompt engineering, deterministic guardrails, and microservice integration "
        "(FastAPI, PostgreSQL), I helped reduce API operating expenses by 40% while delivering robust sub-200ms latency. At the Journal "
        "of Sustainable Energy Systems (JSES), I developed and published prescriptive ML and deep learning models with PyTorch and XGBoost, "
        "translating complex algorithmic requirements into production-ready software."
    )
    story.append(Paragraph(p2, body_style))
    story.append(Spacer(1, 2.5*mm))

    p3 = (
        "I believe that successful AI development requires a balanced blend of strategic thinking, technical depth, and agility. "
        "Whether crafting custom LLM workflows, consulting clients on Generative AI capabilities, or establishing modern DevOps pipelines, "
        "I am dedicated to delivering measurable business value."
    )
    story.append(Paragraph(p3, body_style))
    story.append(Spacer(1, 2.5*mm))

    p4 = (
        "My Bachelor's degree in Computer Engineering is recognized at German Grade 1.5 (Sehr Gut, Anabin H+), granting full qualification "
        "for the fast-track EU Blue Card under the Accelerated Skilled Worker procedure (§ 81a AufenthG). I am excited to relocate to Munich "
        "or collaborate across Mayflower's offices."
    )
    story.append(Paragraph(p4, body_style))
    story.append(Spacer(1, 2.5*mm))

    p5 = (
        "Thank you for considering my application. I would welcome the opportunity to discuss my experience and how I can contribute "
        "to Mayflower's AI initiatives in an interview."
    )
    story.append(Paragraph(p5, body_style))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Sincerely,<br/><b>Sam Moradian</b>", body_style))

    doc.build(story)

build_cover_letter(cl_temp_path)
build_cover_letter(cl_save_path)
print(f"Cover letter built successfully: {cl_temp_path}")
