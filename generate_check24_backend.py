import sys
import shutil
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, r"F:\talentflow-ai")

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

out_dir = Path(r"F:\talentflow-ai\output\CHECK24_4481556177")
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
    textColor=colors.HexColor("#005ea8"),  # CHECK24 blue
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
story.append(Paragraph("Senior Full-Stack Entwickler | Fokus Backend & Distributed Systems", sub_style))
story.append(Paragraph("Shahrak Kowsar, Alley 2, Plot 644, 56196 Ardabil, Iran | +1 (805) 900-7207 | m.hesam.moradian@gmail.com | linkedin.com/in/m-hesam-moradian | github.com/m-hesam-moradian", contact_style))
story.append(hr)

# Summary
story.append(Paragraph("PROFESSIONAL SUMMARY", sec_style))
story.append(Paragraph(
    "Performance-driven Senior Full-Stack Engineer with 4+ years of expertise architecting high-throughput backend services, distributed microservices, "
    "and scalable web systems. Deep technical specialization in Node.js, TypeScript, Python (FastAPI), React/Next.js, PostgreSQL, Apache CouchDB, and Redis. "
    "Proven experience building resilient, asynchronous event-driven pipelines, designing type-safe API gateways (tRPC, GraphQL, REST), and optimizing high-load database queries. "
    "Fully eligible for fast-track relocation to Germany under Section 81a AufenthG and the EU Blue Card with German Grade 1.5 (Sehr Gut, Anabin H+ recognized).",
    body_style
))
story.append(hr)

# Skills
story.append(Paragraph("TECHNICAL EXPERTISE", sec_style))
story.append(Paragraph(
    "<b>Backend Engineering & APIs:</b> Node.js, TypeScript, Express, Python (FastAPI, Flask), RESTful APIs, tRPC, Apollo GraphQL, Microservices, Async Architecture, Token-Bucket Rate Limiting<br/>"
    "<b>Database & Storage Systems:</b> PostgreSQL, CouchDB, Redis (Caching & Session Store), MongoDB, SQL Query Optimization, Data Modeling<br/>"
    "<b>Frontend & Fullstack:</b> React 18, Next.js 14, TypeScript, Tailwind CSS, State Management (Zustand), Responsive UI Design<br/>"
    "<b>DevOps & Infrastructure:</b> Docker, Linux Environments, CI/CD (GitHub Actions), Playwright Automated Testing, GitFlow, Cloud Deployments<br/>"
    "<b>Languages:</b> English (Fluent / C1), German (Proficient / B1-B2), Persian (Native), Turkish (Fluent)",
    body_style
))
story.append(hr)

# Experience
story.append(Paragraph("PROFESSIONAL EXPERIENCE", sec_style))

# Role 1
story.append(Paragraph("<b>Senior Full-Stack Engineer (Lead Developer)</b> — The Million Project | Remote / Germany | Jul 2025 – Present", body_style))
story.append(Paragraph("• Architected and maintained scalable backend services utilizing Next.js 14, tRPC, PostgreSQL, and Redis caching serving 10,000+ monthly active users with sub-200ms P95 latency.", bullet_style))
story.append(Paragraph("• Led migration of legacy endpoints to high-performance modular microservices, reducing payload size by 60% and optimizing database query execution plans.", bullet_style))
story.append(Paragraph("• Implemented automated CI/CD deployment pipelines using GitHub Actions with end-to-end regression suites in Playwright, ensuring 98% deployment uptime.", bullet_style))
story.append(Paragraph("• Mentored junior engineers on clean architecture, type-safety, and concurrent request handling.", bullet_style))

# Role 2
story.append(Paragraph("<b>Machine Learning & Backend Engineer</b> — Journal of Sustainable Energy Systems | Sep 2023 – Jun 2025", body_style))
story.append(Paragraph("• Built high-availability model inference backend using FastAPI and Docker, handling real-time multivariate predictive data streams with <100ms response time.", bullet_style))
story.append(Paragraph("• Engineered automated data ingestion and validation pipelines with Scikit-learn and XGBoost, improving data processing reliability by 70%.", bullet_style))

# Role 3
story.append(Paragraph("<b>Freelance Full-Stack Developer</b> — Karlancer | May 2021 – May 2023", body_style))
story.append(Paragraph("• Delivered 12+ production-grade web applications for corporate clients using React, Node.js, Express, and PostgreSQL.", bullet_style))
story.append(Paragraph("• Built secure IAM microservices featuring JWT token rotation, Redis blacklisting, and OAuth 2.0 authentication flows.", bullet_style))
story.append(hr)

# Education
story.append(Paragraph("EDUCATION & RECOGNITION", sec_style))
story.append(Paragraph("<b>B.Sc. in Computer Software Engineering</b> — Islamic Azad University (Graduated May 2025)", body_style))
story.append(Paragraph("• German Anabin H+ Recognized Institution | Equivalent German GPA: <b>1.5 (Sehr Gut)</b> | Iranian Grade: 18.5 / 20", bullet_style))
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
cl_story.append(Paragraph("Senior Full-Stack Entwickler | Fokus Backend", sub_style))
cl_story.append(Paragraph("Shahrak Kowsar, Alley 2, Plot 644, 56196 Ardabil, Iran | +1 (805) 900-7207 | m.hesam.moradian@gmail.com | linkedin.com/in/m-hesam-moradian", contact_style))
cl_story.append(Spacer(1, 4 * mm))
cl_story.append(hr)
cl_story.append(Spacer(1, 4 * mm))

cl_story.append(Paragraph("<b>Datum:</b> 24. Oktober 2026", cl_body_style))
cl_story.append(Paragraph("<b>An:</b> CHECK24 Vergleichsportal GmbH<br/>Erika-Mann-Straße 62-66, 80636 München, Deutschland", cl_body_style))
cl_story.append(Paragraph("<b>Betreff: Bewerbung als Full-Stack Entwickler (m/w/d) – Fokus Backend Explorer (Ref: ref347d)</b>", sub_style))
cl_story.append(Spacer(1, 2 * mm))

cl_story.append(Paragraph("Sehr geehrte Damen und Herren,", cl_body_style))

cl_story.append(Paragraph(
    "mit großem Interesse bewerbe ich mich auf die Stelle als Full-Stack Entwickler (m/w/d) mit Fokus Backend im Team Explorer bei CHECK24. "
    "Als erfahrener Software Engineer mit über 4 Jahren praktischer Erfahrung in der Entwicklung robuster Backend-Architekturen, "
    "skalierbarer Microservices und performanter Full-Stack-Lösungen möchte ich mein Wissen gewinnbringend bei CHECK24 einbringen.",
    cl_body_style
))

cl_story.append(Paragraph(
    "In meiner aktuellen Rolle als Lead Developer bei The Million Project entwickle und verantworte ich hochperformante Systeme auf Basis von "
    "Node.js, TypeScript, PostgreSQL, Redis und Next.js 14. Durch die Einführung moderner API-Architekturen (tRPC, GraphQL) und datenbankseitiger "
    "Query-Optimierungen konnten wir Latenzzeiten unter 200 ms stabilisieren und Durchsätze bei hoher Nutzerlast signifikant steigern. "
    "Gleichzeitig stelle ich durch automatisierte CI/CD-Pipelines und End-to-End-Tests (Playwright) höchste Codequalität und Release-Sicherheit sicher.",
    cl_body_style
))

cl_story.append(Paragraph(
    "Die Unternehmenskultur von CHECK24 – Schnelligkeit, Agilität, Innovation und exzellente User Experience – spiegelt exakt meinen Arbeitsstil wider. "
    "Ich schätze eigenverantwortliches Arbeiten im agilen Team ebenso wie die pragmatische Lösung komplexer technologischer Herausforderungen.",
    cl_body_style
))

cl_story.append(Paragraph(
    "Hinsichtlich meiner Arbeitserlaubnis und Relocation: Mein B.Sc.-Abschluss in Computer Software Engineering ist in der deutschen Anabin-Datenbank "
    "vollwertig als H+ anerkannt (äquivalente deutsche Gesamtnote: 1.5, Sehr Gut). Ich erfülle alle Voraussetzungen für das beschleunigte "
    "Fachkräfteverfahren (§ 81a AufenthG) sowie die Blaue Karte EU. Meine Gehaltserwartung liegt bei 85.000 € brutto/Jahr, und ich stehe für "
    "einen Arbeitsantritt ab sofort zur Verfügung.",
    cl_body_style
))

cl_story.append(Paragraph(
    "Ich freue mich über die Gelegenheit zu einem persönlichen Gespräch.",
    cl_body_style
))

cl_story.append(Paragraph("Mit freundlichen Grüßen,<br/><b>Sam Moradian</b>", cl_body_style))

cl_doc.build(cl_story)
print(f"Cover Letter generated: {cl_path}")

# Stage to Temp with strict naming
staged_cv = temp_dir / "Sam_Moradian_CV.pdf"
staged_cl = temp_dir / "Sam_Moradian_Cover_Letter.pdf"

shutil.copy2(cv_path, staged_cv)
shutil.copy2(cl_path, staged_cl)

print(f"Staged CV to: {staged_cv}")
print(f"Staged Cover Letter to: {staged_cl}")
