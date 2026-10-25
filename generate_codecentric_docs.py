import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import mm

temp_dir = Path(r"C:\Users\Sam\AppData\Local\Temp")
temp_dir.mkdir(parents=True, exist_ok=True)

output_dir = Path(r"F:\talentflow-ai\output\codecentric_4453087296")
output_dir.mkdir(parents=True, exist_ok=True)

# 1. GENERATE CV
cv_temp_path = temp_dir / "Sam_Moradian_CV.pdf"
cv_save_path = output_dir / "Sam_Moradian_CV.pdf"

styles = getSampleStyleSheet()

primary_color = colors.HexColor("#007ACC") # codecentric Blue
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
    story.append(Paragraph("Senior AI-Native Software Architect & Engineer | Agentic Systems & SSDLC", title_style))
    contact_info = "Ardabil, Iran (EU Blue Card & Fast-Track § 81a AufenthG Eligible) | +1 805 900 7207 | m.hesam.moradian@gmail.com | linkedin.com/in/m-hesam-moradian | github.com/m-hesam-moradian"
    story.append(Paragraph(contact_info, contact_style))
    story.append(Spacer(1, 2*mm))
    story.append(HRFlowable(width="100%", thickness=0.75, color=primary_color, spaceAfter=4, spaceBefore=2))

    # Profile Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
    summary_text = (
        "Forward-thinking Senior Software Architect & AI Engineer with 5+ years of experience transforming software delivery "
        "through AI-native architectures, multi-agent frameworks (LangGraph, LiteLLM), and secure engineering practices (SSDLC). "
        "A true T-shaped engineer with deep expertise in Python, TypeScript, modern cloud architectures, and distributed systems. "
        "Passionate about shaping how AI elevates software engineering from experimentation into measurable business value. "
        "Fully eligible for the accelerated EU Blue Card under the Fast-Track Skilled Worker program (§ 81a AufenthG)."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceAfter=4, spaceBefore=4))

    # Core Competencies
    story.append(Paragraph("CORE COMPETENCIES & TECHNICAL EXPERTISE", section_heading))
    skills = [
        "<b>Architectures & Paradigms:</b> AI-Native Architecture, Multi-Agent Systems, Event-Driven Design, Microservices, SSDLC",
        "<b>Languages & Frameworks:</b> Python (FastAPI, Flask), TypeScript/JavaScript (Node.js, React, Next.js), SQL",
        "<b>AI/ML Ecosystem:</b> LangGraph, LiteLLM, LangChain, PyTorch, Scikit-learn, XGBoost, Model Routing, Evaluation & Guardrails",
        "<b>Cloud & DevOps:</b> Docker, Kubernetes, CI/CD (GitHub Actions), PostgreSQL, Redis, CouchDB, REST APIs, GraphQL"
    ]
    for sk in skills:
        story.append(Paragraph(f"• {sk}", bullet_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceAfter=4, spaceBefore=4))

    # Professional Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_heading))

    story.append(Paragraph("<b>The Million Project</b> | Senior Full-Stack & AI Systems Architect | 2024 – Present", bold_body))
    exp1 = [
        "Architected multi-agent LangGraph pipelines integrated with LiteLLM routing and automated guardrails, cutting LLM operational costs by 40%.",
        "Engineered scalable Next.js + tRPC + PostgreSQL cloud platforms handling 10,000+ monthly active users at sub-200ms P95 latency.",
        "Embedded automated security, static analysis, and end-to-end testing into GitHub Actions CI/CD pipelines, driving a 98% deployment success rate."
    ]
    for b in exp1:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("<b>Journal of Sustainable Energy Systems (JSES)</b> | Machine Learning & Deep Learning Engineer | 2023 – Present", bold_body))
    exp2 = [
        "Designed and published prescriptive AI pipelines combining XGBoost, Elastic Net regression, and causal inference for grid forecasting.",
        "Built robust PyTorch deep learning models integrated into production FastAPI microservices delivering real-time inferences.",
        "Engineered automated data extraction, feature engineering, and validation workflows that reduced pipeline runtimes by 70%."
    ]
    for b in exp2:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("<b>Independent / Freelance</b> | Senior Software & AI Engineer | 2021 – 2024", bold_body))
    exp3 = [
        "Architected and deployed 15+ production full-stack web applications and AI tools for international clients across Europe and North America.",
        "Implemented secure JWT authentication systems, RESTful microservices, and automated testing suites."
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
        "<b>codecentric AG</b><br/>"
        "People & Culture / Engineering Hiring Team<br/>"
        "Hochstraße 11<br/>"
        "42697 Solingen, Germany<br/><br/>"
        "<b>Application for: Senior AI-Native Software Architect / Engineer (w/d/m) (Ref. 2625981)</b>"
    )
    story.append(Paragraph(recipient_info, body_style))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Dear Hiring Team at codecentric AG,", ParagraphStyle("Salutation", parent=body_style, fontName="Helvetica-Bold")))
    story.append(Spacer(1, 2*mm))

    p1 = (
        "I am writing to express my strong enthusiasm for the <b>Senior AI-Native Software Architect / Engineer (w/d/m)</b> "
        "position at codecentric AG. As an engineer passionate about how AI transforms the software engineering lifecycle—from "
        "initial system architecture to the Secure Software Development Life Cycle (SSDLC)—codecentric's philosophy of being "
        "thought leaders, techies, and trusted sparring partners for enterprise clients resonates deeply with my vision."
    )
    story.append(Paragraph(p1, body_style))
    story.append(Spacer(1, 2.5*mm))

    p2 = (
        "Over the past 5+ years, I have architected both scalable full-stack applications and sophisticated AI systems. At The Million "
        "Project, I lead the development of multi-agent LangGraph pipelines routed via LiteLLM with strict latency and cost guardrails, "
        "lowering API costs by 40% while preserving high deterministic reliability. In tandem, through published research at the Journal "
        "of Sustainable Energy Systems (JSES), I have developed prescriptive ML and deep learning architectures with PyTorch and FastAPI, "
        "bridging algorithmic innovation with real-world operational execution."
    )
    story.append(Paragraph(p2, body_style))
    story.append(Spacer(1, 2.5*mm))

    p3 = (
        "My approach to software engineering has always been T-shaped: combining a solid foundation in modern backend (Python, FastAPI, "
        "PostgreSQL, Docker) and frontend (TypeScript, React, Next.js) with cutting-edge AI orchestration paradigms. I am thrilled by the "
        "opportunity to join codecentric's AI-Augmented Engineering cluster, shaping best practices and helping clients rethink their "
        "software value chains."
    )
    story.append(Paragraph(p3, body_style))
    story.append(Spacer(1, 2.5*mm))

    p4 = (
        "My Bachelor's degree in Computer Engineering is evaluated at German Grade 1.5 (Sehr Gut, Anabin H+), granting full eligibility "
        "for the fast-track EU Blue Card (§ 81a AufenthG). I am ready to relocate to Germany immediately and look forward to contributing "
        "to codecentric's projects across any location or in hybrid setups."
    )
    story.append(Paragraph(p4, body_style))
    story.append(Spacer(1, 2.5*mm))

    p5 = (
        "Thank you very much for your time and consideration. I would be delighted to discuss my background and ideas with you in an interview."
    )
    story.append(Paragraph(p5, body_style))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Sincerely,<br/><b>Sam Moradian</b>", body_style))

    doc.build(story)

build_cover_letter(cl_temp_path)
build_cover_letter(cl_save_path)
print(f"Cover letter built successfully: {cl_temp_path}")
