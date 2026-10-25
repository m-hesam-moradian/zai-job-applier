import sys
import shutil
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, r"F:\talentflow-ai")

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle

out_dir = Path(r"F:\talentflow-ai\output\adesso_SE_4473727917")
out_dir.mkdir(parents=True, exist_ok=True)

temp_dir = Path(r"C:\Users\Sam\AppData\Local\Temp")

cv_path = out_dir / "Sam_Moradian_CV.pdf"
cl_path = out_dir / "Sam_Moradian_Cover_Letter.pdf"

# -------------------------------------------------------------
# Generate CV
# -------------------------------------------------------------
doc = SimpleDocTemplate(
    str(cv_path),
    pagesize=A4,
    leftMargin=14 * mm,
    rightMargin=14 * mm,
    topMargin=12 * mm,
    bottomMargin=12 * mm,
)

styles = getSampleStyleSheet()

name_style = ParagraphStyle(
    "Name",
    parent=styles["Heading1"],
    fontSize=18,
    leading=22,
    textColor=colors.HexColor("#0f172a"),
    fontName="Helvetica-Bold",
    spaceAfter=2,
)

sub_style = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontSize=10.5,
    leading=14,
    textColor=colors.HexColor("#1e40af"),
    fontName="Helvetica-Bold",
    spaceAfter=4,
)

contact_style = ParagraphStyle(
    "Contact",
    parent=styles["Normal"],
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor("#475569"),
    spaceAfter=4,
)

sec_style = ParagraphStyle(
    "Section",
    parent=styles["Heading2"],
    fontSize=11,
    leading=14,
    textColor=colors.HexColor("#0f172a"),
    fontName="Helvetica-Bold",
    spaceBefore=5,
    spaceAfter=3,
)

body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontSize=8.5,
    leading=11.5,
    textColor=colors.HexColor("#1e293b"),
    spaceAfter=3,
)

bullet_style = ParagraphStyle(
    "Bullet",
    parent=styles["Normal"],
    fontSize=8.5,
    leading=11.5,
    textColor=colors.HexColor("#334155"),
    leftIndent=10,
    spaceAfter=1.5,
)

hr = HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#cbd5e1"), spaceBefore=3, spaceAfter=4)

story = []

# Header
story.append(Paragraph("Sam Moradian", name_style))
story.append(Paragraph("Forward Deployed Engineer | Agentic AI Systems & Enterprise Full-Stack Architect", sub_style))
story.append(Paragraph("Ardabil, Iran (Eligible for EU Blue Card & Fast-Track Section 81a AufenthG) | +1 (805) 900-7207 | m.hesam.moradian@gmail.com | linkedin.com/in/m-hesam-moradian | github.com/m-hesam-moradian", contact_style))
story.append(hr)

# Summary
story.append(Paragraph("PROFESSIONAL SUMMARY", sec_style))
story.append(Paragraph(
    "High-impact Forward Deployed AI Engineer and Full-Stack Architect with 4+ years of expertise delivering enterprise multi-agent workflows, "
    "autonomous coding systems, and cloud architectures. Track record of developing and deploying 5+ production AI agents with measurable business impact, "
    "integrating LLM orchestration (LangGraph, LiteLLM, MCP) with high-availability web stacks (Next.js, React, FastAPI, Node.js/TypeScript, Python). "
    "Experienced in partnering directly with enterprise stakeholders, bridging technical and business requirements, and driving rapid prototyping from ideation to production. "
    "Fully eligible for the German EU Blue Card and Fast-Track Visa (Section 81a AufenthG) with German Grade 1.5 (Sehr Gut, Anabin H+).",
    body_style
))
story.append(hr)

# Skills
story.append(Paragraph("TECHNICAL EXPERTISE", sec_style))
story.append(Paragraph(
    "<b>Agentic AI & Orchestration:</b> LangGraph, LiteLLM, Multi-Agent Systems, Model Context Protocol (MCP), Autonomous Coding Agents, Prompt Engineering, RAG, PyTorch, Scikit-learn, XGBoost<br/>"
    "<b>Full-Stack & Cloud Architecture:</b> Python (FastAPI, Flask), TypeScript, JavaScript, React 18, Next.js 14, Node.js, RESTful APIs, tRPC, GraphQL, Docker, Microservices, CI/CD (GitHub Actions)<br/>"
    "<b>Databases & Infrastructure:</b> PostgreSQL, CouchDB, Redis, MongoDB, Linux Systems, AWS/Cloud Deployments, Playwright Automation<br/>"
    "<b>Languages:</b> English (Fluent / C1), German (Proficient / B1-B2), Persian (Native), Turkish (Fluent)",
    body_style
))
story.append(hr)

# Experience
story.append(Paragraph("PROFESSIONAL EXPERIENCE", sec_style))

# Role 1
story.append(Paragraph("<b>Senior Full-Stack & AI Systems Lead</b> — The Million Project | Remote / Germany | Jul 2025 – Present", body_style))
story.append(Paragraph("• Architected and brought to production multi-agent LangGraph & LiteLLM pipelines with intelligent fallback and model routing, decreasing LLM operational costs by 40% while accelerating pipeline throughput.", bullet_style))
story.append(Paragraph("• Delivered rapid enterprise prototypes using Agentic Coding workflows, scaling Next.js 14, TypeScript, and PostgreSQL platforms to 10k+ monthly active users with sub-200ms response times.", bullet_style))
story.append(Paragraph("• Bridged business stakeholders and engineering teams, translating domain requirements into concrete technical specifications and production AI agent microservices.", bullet_style))
story.append(Paragraph("• Established robust automated testing and CI/CD pipelines with GitHub Actions and Playwright E2E suites, maintaining a 98% deployment success rate.", bullet_style))

# Role 2
story.append(Paragraph("<b>Machine Learning & Deep Learning Engineer</b> — Journal of Sustainable Energy Systems | Sep 2023 – Jun 2025", body_style))
story.append(Paragraph("• Designed and deployed predictive AI pipelines utilizing XGBoost, PyTorch, and causal inference models for energy demand forecasting, published in peer-reviewed scientific literature.", bullet_style))
story.append(Paragraph("• Built automated feature engineering and model serving microservices using FastAPI and Docker, achieving low-latency model inference (<100ms P95).", bullet_style))
story.append(Paragraph("• Implemented explainable AI frameworks (SHAP, LIME) to validate predictive outputs with domain specialists and non-technical stakeholders.", bullet_style))

# Role 3
story.append(Paragraph("<b>Full-Stack Software Engineer</b> — Freelance / Karlancer | May 2021 – May 2023", body_style))
story.append(Paragraph("• Engineered 12+ custom web applications and enterprise portals using React, TypeScript, Node.js, and relational databases, ensuring 99.9% uptime and high Lighthouse scores.", bullet_style))
story.append(Paragraph("• Developed modular REST and GraphQL APIs, JWT/OAuth authentication workflows, and third-party SaaS integrations for client organizations.", bullet_style))
story.append(hr)

# Key AI Projects
story.append(Paragraph("KEY AGENTIC AI PROJECTS", sec_style))
story.append(Paragraph("<b>TalentFlow-AI:</b> Autonomous multi-agent career & document orchestrator utilizing LangGraph, LiteLLM, MCP, and Playwright for real-time ATS scoring, resume adaptation, and automated application dispatch.", bullet_style))
story.append(Paragraph("<b>Enterprise Auth & Agent Microservice:</b> Token-bucket authenticated microservice handling high-throughput session state, Redis caching, and autonomous monitoring agents.", bullet_style))
story.append(hr)

# Education
story.append(Paragraph("EDUCATION & RECOGNITION", sec_style))
story.append(Paragraph("<b>B.Sc. in Computer Software Engineering</b> — Islamic Azad University (Graduated May 2025)", body_style))
story.append(Paragraph("• German Anabin H+ Recognized Degree | Equivalent German GPA: <b>1.5 (Sehr Gut)</b> | Iranian Grade: 18.5 / 20", bullet_style))
story.append(Paragraph("<b>CS50x: Computer Science</b> — Harvard University (Certified Jan 2024)", body_style))

doc.build(story)
print(f"CV generated: {cv_path}")

# -------------------------------------------------------------
# Generate Cover Letter
# -------------------------------------------------------------
cl_doc = SimpleDocTemplate(
    str(cl_path),
    pagesize=A4,
    leftMargin=20 * mm,
    rightMargin=20 * mm,
    topMargin=20 * mm,
    bottomMargin=20 * mm,
)

cl_story = []

cl_title_style = ParagraphStyle(
    "CLTitle",
    parent=styles["Heading1"],
    fontSize=16,
    leading=20,
    textColor=colors.HexColor("#0f172a"),
    fontName="Helvetica-Bold",
    spaceAfter=4,
)

cl_body_style = ParagraphStyle(
    "CLBody",
    parent=styles["Normal"],
    fontSize=10,
    leading=15,
    textColor=colors.HexColor("#1e293b"),
    spaceAfter=10,
)

cl_story.append(Paragraph("Sam Moradian", cl_title_style))
cl_story.append(Paragraph("Forward Deployed Engineer | Agentic AI Systems Architect", sub_style))
cl_story.append(Paragraph("Ardabil, Iran | +1 (805) 900-7207 | m.hesam.moradian@gmail.com | linkedin.com/in/m-hesam-moradian", contact_style))
cl_story.append(Spacer(1, 4 * mm))
cl_story.append(hr)
cl_story.append(Spacer(1, 4 * mm))

cl_story.append(Paragraph("<b>Date:</b> October 24, 2026", cl_body_style))
cl_story.append(Paragraph("<b>To:</b> Recruiting Team | adesso SE<br/>Adessoplatz 1, 44269 Dortmund, Germany", cl_body_style))
cl_story.append(Paragraph("<b>Subject: Application for Forward Deployed Engineer (all genders) — Job ID: 22159</b>", sub_style))
cl_story.append(Spacer(1, 2 * mm))

cl_story.append(Paragraph("Dear Recruiting Team at adesso SE,", cl_body_style))

cl_story.append(Paragraph(
    "I am writing to express my strong enthusiasm for the Forward Deployed Engineer (all genders) position at adesso SE. "
    "With a proven background bridging enterprise software architecture, agentic AI frameworks, and client-facing project delivery, "
    "I am eager to help adesso's clients transform technological possibilities into high-impact, production-ready AI agent solutions.",
    cl_body_style
))

cl_story.append(Paragraph(
    "Throughout my career as a Senior Full-Stack and AI Systems Engineer, I have built and deployed over five autonomous agent workflows "
    "and multi-agent systems with demonstrable business impact. At The Million Project, I engineered LangGraph and LiteLLM orchestration pipelines "
    "that reduced operational LLM costs by 40% while automating mission-critical workflows across Next.js, TypeScript, and PostgreSQL microservices. "
    "My hands-on experience in Agentic Coding enables me to rapidly prototype custom enterprise applications and bring intelligent agents into "
    "reliable production within weeks.",
    cl_body_style
))

cl_story.append(Paragraph(
    "The Forward Deployed Engineer role at adesso SE resonates deeply with my core strengths: identifying business processes ripe for AI automation, "
    "collaborating directly with stakeholders and C-level decision-makers, and integrating cross-functional teams to ensure lasting project adoption. "
    "Whether architecting robust Python/FastAPI backends, TypeScript/React frontends, or integrating enterprise data sources via Model Context Protocol (MCP), "
    "I ensure that technological depth is paired with clear business value.",
    cl_body_style
))

cl_story.append(Paragraph(
    "Regarding visa authorization and relocation: my B.Sc. in Computer Software Engineering holds full H+ recognition in the German Anabin database "
    "with an equivalent German Grade of 1.5 (Sehr Gut). I am fully eligible for the German EU Blue Card and the Accelerated Skilled Worker Procedure "
    "(Section 81a AufenthG), enabling streamlined relocation to Germany. I possess proficient German language skills (B1/B2) alongside fluent English (C1).",
    cl_body_style
))

cl_story.append(Paragraph(
    "I would welcome the opportunity to discuss how my technical expertise in agentic frameworks, rapid prototyping, and client collaboration "
    "can drive impactful results for adesso SE and your enterprise clients.",
    cl_body_style
))

cl_story.append(Paragraph("Sincerely,<br/><b>Sam Moradian</b>", cl_body_style))

cl_doc.build(cl_story)
print(f"Cover Letter generated: {cl_path}")

# Stage to Temp with strict naming
staged_cv = temp_dir / "Sam_Moradian_CV.pdf"
staged_cl = temp_dir / "Sam_Moradian_Cover_Letter.pdf"

shutil.copy2(cv_path, staged_cv)
shutil.copy2(cl_path, staged_cl)

print(f"Staged CV to: {staged_cv}")
print(f"Staged Cover Letter to: {staged_cl}")
