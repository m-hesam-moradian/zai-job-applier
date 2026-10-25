"""Pixel-perfect HTML/CSS CV Template replicating Google Slides Main CV.svg 1:1."""
from __future__ import annotations

import base64
from pathlib import Path
import re
from typing import Any

from src.schemas.models import DynamicCandidateProfile, TailoredApplicationPackage

ROOT_DIR = Path(__file__).parent.parent.parent
AVATAR_PATH = ROOT_DIR / "data" / "extracted_image_0.png"


def _get_avatar_base64() -> str:
    """Return base64 data URI of the candidate avatar."""
    if AVATAR_PATH.exists():
        data = AVATAR_PATH.read_bytes()
        b64 = base64.b64encode(data).decode("ascii")
        return f"data:image/png;base64,{b64}"
    return ""


def _build_skill_categories_html(package: TailoredApplicationPackage | None) -> str:
    category_pools = [
        ("SPOKEN LANGUAGES", ["English (B2/C1)", "German (A2/B1)", "Turkish (C1)", "Persian (C2)"]),
        ("PROGRAMMING LANGUAGES", ["TypeScript", "Python", "JavaScript (ES6+)", "SQL", "C++", "Solidity"]),
        ("FRONTEND DEVELOPMENT", ["Next.js", "React.js", "Tailwind CSS", "ShadCN", "Radix UI", "TanStack Query", "Zod", "MUI", "Three.js"]),
        ("BACKEND & APIS", ["Node.js", "NestJS", "FastAPI", "Express.js", "RESTful APIs", "tRPC", "Apollo GraphQL", "IAM/SSO", "OAuth2/JWT"]),
        ("DATABASES & ORM", ["Vector DBs (Pinecone/Weaviate)", "PostgreSQL", "Apache CouchDB", "MongoDB", "Redis", "MySQL", "Prisma ORM"]),
        ("AI & MACHINE LEARNING", ["LLMs & AI APIs", "AI Agents & Workflows", "RAG & Vector Search", "Prompt Engineering", "LangGraph", "PyTorch", "TensorFlow", "Transformers", "LiteLLM"]),
        ("INFRASTRUCTURE & CLOUD", ["GCP (Google Cloud)", "Docker", "Docker Compose", "CI/CD (GitHub Actions)", "Vitest", "Traefik", "Git", "Linux/SSL"]),
    ]

    jd_keywords = set()
    if package:
        raw_text = f"{package.job_title} {' '.join(package.selected_skills[:25])}".lower()
        jd_keywords = {w for w in re.findall(r"[a-z0-9_\-\.+#]+", raw_text) if len(w) >= 2}

    html_blocks = []
    for cat_title, pool in category_pools:
        if jd_keywords:
            def _item_score(item: str) -> int:
                it_l = item.lower()
                return sum(1 for kw in jd_keywords if kw in it_l)
            sorted_pool = sorted(pool, key=_item_score, reverse=True)
        else:
            sorted_pool = pool

        body_text = ", ".join(sorted_pool[:7])
        html_blocks.append(f"""      <div class="skill-category">\n        <div class="skill-cat-title">{cat_title}</div>\n        <div class="skill-cat-body">{body_text}</div>\n      </div>""")

    return "\n\n".join(html_blocks)


def render_cv_html(
    profile: DynamicCandidateProfile,
    package: TailoredApplicationPackage | None = None,
) -> str:
    """Render the exact 2-column CV layout matching Main CV.svg."""
    avatar_src = _get_avatar_base64()

    # Dynamic or seed summary
    if package and package.tailored_summary:
        summary_text = package.tailored_summary
    else:
        summary_text = (
            "Full-Stack AI Engineer with over 4 years of experience unifying high-concurrency web "
            "platforms with production-grade machine learning pipelines and secure cloud infrastructure. "
            "Expert in architecting modular Identity & Access Management (IAM/SSO) microservices, "
            "type-safe API gateways, and scalable Next.js/React frontends backed by Apache CouchDB and Redis. "
            "Deeply skilled in engineering statistical ML/DL pipelines using PyTorch and TensorFlow, "
            "integrating Explainable AI (SHAP, LIME, Morris FAST), and designing uncertainty quantification "
            "models for enterprise decision-making. Certified by Harvard University (CS50x) with a strong "
            "foundation in clean architecture, deterministic state alignment, and scalable team leadership."
        )

    # Dynamic or seed headline
    headline = "Full-Stack AI Engineer"
    if package and package.tailored_headline:
        headline = package.tailored_headline

    # Professional experience data
    dt = profile.dynamic_template
    bullets_million = (
        package.tailored_bullets.get("role_million_project")
        if package and package.tailored_bullets
        else None
    ) or dt.experience_bullets.get("role_million_project", [
        "End-to-End Platform Architecture: Engineered high-concurrency social media MVP under tight deadlines, managing complete end-to-end development, automated testing (Vitest), and CI/CD via Docker.",
        "Complex API Integration: Designed secure, scalable custom APIs using tRPC, Apollo GraphQL, and REST to integrate backend infrastructure, authentication, and Apache CouchDB with Wix.",
        "High-Performance Frontend: Built modular, accessible UIs utilizing Next.js, React, TypeScript, Tailwind CSS, and Radix UI with strict Zod validation.",
        "Leadership & Mentorship: Transitioned to Lead Developer; recruited, mentored, and delegated architectural tasks to junior developers to optimize system scalability.",
    ])

    bullets_jses = (
        package.tailored_bullets.get("role_jses")
        if package and package.tailored_bullets
        else None
    ) or dt.experience_bullets.get("role_jses", [
        "AI Architecture & Pipeline Engineering: Deployed predictive ML/DL models (Random Forest, XGBoost, CNNs, LSTMs, Transformers) utilizing TensorFlow and PyTorch.",
        "System Reliability & Explainability: Hardened AI components by implementing advanced explainability (SHAP, LIME) and uncertainty calibration techniques for enterprise-grade decision-making.",
        "Production Integration: Bridged theoretical data science and software engineering, structuring complex ML models for secure, scalable integration into business workflows.",
        "Algorithmic Optimization: Enhanced model accuracy and generalization via custom K-Fold Cross Validation, advanced feature engineering, and hyperparameter optimization.",
    ])

    bullets_karlancer = (
        package.tailored_bullets.get("role_freelance")
        if package and package.tailored_bullets
        else None
    ) or dt.experience_bullets.get("role_freelance", [
        "End-to-End System Design: Architected a production-ready, highly scalable full-stack e-commerce platform leveraging React, Next.js, Node.js, and Express.js.",
        "API Design & Type Safety: Ensured strict end-to-end type safety using TypeScript and tRPC alongside state management via React Query (TanStack).",
        "System Refactoring & Code Quality: Optimally engineered application performance and maintainability by implementing clean architecture and reusable design patterns.",
    ])

    skills_categories_html = _build_skill_categories_html(package)

    bullets_arman = [
        "UI/UX Implementation: Developed pixel-perfect, responsive website UIs from scratch, engineering dynamic navigation, product filtering, and interactive components.",
        "Platform Modernization: Spearheaded migration of vanilla JS codebase to React and Tailwind CSS, applying custom hooks and component composition.",
        "Frontend Architecture: Delivered high-performance application by resolving complex front-end challenges and adhering to clean code standards.",
    ]

    def format_bullets(bullets: list[str]) -> str:
        html = []
        for b in bullets:
            if ":" in b:
                lead, rest = b.split(":", 1)
                html.append(f'<li><span class="bullet-lead">{lead.strip()}:</span>{rest}</li>')
            else:
                html.append(f"<li>{b}</li>")
        return "\n".join(html)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>SAM MORADIAN - CV</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    @page {{
      size: A4 portrait;
      margin: 0;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}

    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      width: 210mm;
      height: 297mm;
      max-height: 297mm;
      margin: 0 auto;
      background: #FFFFFF;
      color: #334155;
      display: flex;
      flex-direction: row;
      overflow: hidden;
      font-size: 8.5px;
      line-height: 1.35;
    }}

    /* ==========================================================================
       LEFT SIDEBAR (Width: 63.5mm / ~30.2% of A4)
       ========================================================================== */
    .sidebar {{
      width: 63.5mm;
      height: 297mm;
      background: #E2E8F0;
      border-right: 1px solid #CBD5E1;
      padding: 10mm 5mm 6mm 6mm;
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }}

    .avatar-container {{
      display: flex;
      justify-content: center;
      margin-bottom: 5mm;
    }}

    .avatar {{
      width: 28mm;
      height: 28mm;
      border-radius: 50%;
      border: 2.2px solid #06B6D4;
      object-fit: cover;
      display: block;
      background: #FFFFFF;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }}

    .sidebar-section {{
      margin-bottom: 3.5mm;
    }}

    .sidebar-title {{
      font-size: 8.2px;
      font-weight: 800;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      color: #0F172A;
      border-bottom: 1.2px solid #94A3B8;
      padding-bottom: 1.2px;
      margin-bottom: 2mm;
    }}

    /* Contact Links */
    .contact-list {{
      list-style: none;
    }}

    .contact-item {{
      display: flex;
      align-items: center;
      gap: 5px;
      margin-bottom: 1.6mm;
      font-size: 7.6px;
    }}

    .contact-item svg {{
      width: 9px;
      height: 9px;
      color: #06B6D4;
      flex-shrink: 0;
    }}

    .contact-link {{
      color: #0097A7;
      text-decoration: underline;
      text-decoration-color: #0097A7;
      text-underline-offset: 1.5px;
      word-break: break-all;
    }}

    /* Education */
    .edu-degree {{
      font-size: 8px;
      font-weight: 700;
      color: #0F172A;
    }}

    .edu-school {{
      font-size: 7.6px;
      color: #0097A7;
      text-decoration: underline;
      text-decoration-color: #0097A7;
      font-weight: 600;
      margin-bottom: 0.8mm;
      display: inline-block;
    }}

    .edu-dates {{
      font-size: 7px;
      color: #64748B;
      margin-bottom: 1.2mm;
    }}

    .grade-title {{
      font-size: 7.2px;
      font-weight: 700;
      color: #0F172A;
      margin-top: 0.8mm;
    }}

    .grade-list {{
      list-style: none;
      padding-left: 2px;
      font-size: 7px;
      line-height: 1.35;
      color: #334155;
    }}

    .grade-list li::before {{
      content: "• ";
      color: #06B6D4;
      font-weight: bold;
    }}

    .anabin-badge {{
      margin-top: 1.2mm;
      font-size: 6.8px;
      font-weight: 700;
      color: #0369A1;
      background: #E0F2FE;
      padding: 1.5px 3.5px;
      border-radius: 2px;
      display: inline-block;
      border: 0.5px solid #BAE6FD;
    }}

    /* Certificate */
    .cert-title {{
      font-size: 8px;
      font-weight: 700;
      color: #0F172A;
    }}

    .cert-issuer {{
      font-size: 7.2px;
      color: #0097A7;
      font-weight: 600;
      text-decoration: underline;
      text-decoration-color: #0097A7;
    }}

    .cert-meta {{
      font-size: 6.8px;
      color: #64748B;
      margin-top: 0.5mm;
    }}

    /* Skills */
    .skill-category {{
      margin-bottom: 2mm;
    }}

    .skill-cat-title {{
      font-size: 7px;
      font-weight: 800;
      color: #0F172A;
      letter-spacing: 0.4px;
      text-transform: uppercase;
      margin-bottom: 0.6mm;
    }}

    .skill-cat-body {{
      font-size: 6.8px;
      line-height: 1.3;
      color: #334155;
    }}

    /* ==========================================================================
       RIGHT MAIN CONTENT (Width: 146.5mm / ~69.8% of A4)
       ========================================================================== */
    .main {{
      width: 146.5mm;
      height: 297mm;
      padding: 8mm 8mm 6mm 8mm;
      display: flex;
      flex-direction: column;
      flex-grow: 1;
    }}

    /* Header */
    .header {{
      margin-bottom: 3.5mm;
    }}

    .candidate-name {{
      font-size: 22pt;
      font-weight: 800;
      letter-spacing: 0.5px;
      color: #0F172A;
      line-height: 1.05;
      text-transform: uppercase;
    }}

    .candidate-title {{
      font-size: 11pt;
      font-weight: 700;
      color: #06B6D4;
      margin-top: 1mm;
      margin-bottom: 2.2mm;
    }}

    .summary-text {{
      font-size: 7.6px;
      line-height: 1.35;
      color: #334155;
      text-align: justify;
    }}

    /* Main Section Headers */
    .section-title {{
      font-size: 9.5pt;
      font-weight: 800;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      color: #0F172A;
      border-bottom: 1.5px solid #06B6D4;
      padding-bottom: 1.2px;
      margin-top: 2.5mm;
      margin-bottom: 2.5mm;
    }}

    /* Job Card */
    .job-card {{
      margin-bottom: 2.8mm;
    }}

    .job-header {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 0.4mm;
    }}

    .job-role {{
      font-size: 8.5px;
      font-weight: 700;
      color: #0F172A;
    }}

    .job-dates {{
      font-size: 7.2px;
      color: #64748B;
      font-weight: 500;
    }}

    .job-company {{
      font-size: 7.8px;
      font-weight: 600;
      color: #0097A7;
      text-decoration: underline;
      text-decoration-color: #0097A7;
      text-underline-offset: 1.2px;
      margin-bottom: 1.2mm;
      display: inline-block;
    }}

    .job-bullets {{
      list-style: none;
      padding-left: 0;
    }}

    .job-bullets li {{
      position: relative;
      padding-left: 9px;
      font-size: 7.2px;
      line-height: 1.32;
      color: #334155;
      margin-bottom: 1mm;
      text-align: justify;
    }}

    .job-bullets li::before {{
      content: "●";
      position: absolute;
      left: 0;
      top: 0.5px;
      font-size: 5px;
      color: #0F172A;
    }}

    .bullet-lead {{
      font-weight: 700;
      color: #0F172A;
      margin-right: 2px;
    }}
  </style>
</head>
<body>

  <!-- ======================== LEFT SIDEBAR ======================== -->
  <aside class="sidebar">
    <div class="avatar-container">
      <img class="avatar" src="{avatar_src}" alt="Sam Moradian">
    </div>

    <!-- CONTACT -->
    <div class="sidebar-section">
      <div class="sidebar-title">CONTACT</div>
      <ul class="contact-list">
        <li class="contact-item">
          <svg fill="currentColor" viewBox="0 0 24 24"><path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2a1 1 0 011.02-.24 11.72 11.72 0 003.68.59 1 1 0 011 1v3.5a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1 11.72 11.72 0 00.59 3.68 1 1 0 01-.24 1.02l-2.23 2.09z"/></svg>
          <a class="contact-link" href="tel:+18059007207">+1(805)900-7207</a>
        </li>
        <li class="contact-item">
          <svg fill="currentColor" viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
          <a class="contact-link" href="mailto:m.hesam.moradian@gmail.com">m.hesam.moradian@gmail</a>
        </li>
        <li class="contact-item">
          <svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
          <a class="contact-link" href="https://github.com/m-hesam-moradian" target="_blank">Github</a>
        </li>
        <li class="contact-item">
          <svg fill="currentColor" viewBox="0 0 24 24"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>
          <a class="contact-link" href="https://www.linkedin.com/in/m-hesam-moradian/" target="_blank">LinkedIn</a>
        </li>
        <li class="contact-item">
          <svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 010-5 2.5 2.5 0 010 5z"/></svg>
          <a class="contact-link" href="https://share.google/sEGJfnDjc4caNsZbd" target="_blank">Ardabil, Iran</a>
        </li>
      </ul>
    </div>

    <!-- EDUCATION -->
    <div class="sidebar-section">
      <div class="sidebar-title">EDUCATION</div>
      <div class="edu-degree">B.S. Computer Engineering</div>
      <a class="edu-school" href="https://iau.ir/en" target="_blank">Islamic Azad University (IAU)</a>
      <div class="edu-dates">Sep 2021 – May 2025 | Ardabil</div>
      <div class="grade-title">Grade Equivalency:</div>
      <ul class="grade-list">
        <li>Iran: 18.5 / 20</li>
        <li>USA (GPA): ≈ 3.8 / 4.0</li>
        <li>Germany: 1.5 (Sehr Gut)</li>
      </ul>
      <div class="anabin-badge">★ H+ status in German Anabin database</div>
    </div>

    <!-- CERTIFICATE -->
    <div class="sidebar-section">
      <div class="sidebar-title">CERTIFICATE</div>
      <div class="cert-title">CS50x: Computer Science</div>
      <div class="cert-issuer">Harvard University — Jan 2024</div>
      <div class="cert-meta">ID: fe673d2f-6a44-46b...</div>
    </div>

    <!-- SKILLS -->
    <div class="sidebar-section">
      <div class="sidebar-title">SKILLS</div>

{skills_categories_html}
    </div>
  </aside>

  <!-- ======================== RIGHT MAIN ======================== -->
  <main class="main">
    <header class="header">
      <h1 class="candidate-name">SAM MORADIAN</h1>
      <div class="candidate-title">{headline}</div>
      <p class="summary-text">{summary_text}</p>
    </header>

    <section>
      <h2 class="section-title">PROFESSIONAL EXPERIENCE</h2>

      <!-- The Million Project -->
      <article class="job-card">
        <div class="job-header">
          <span class="job-role">Senior Full-Stack Engineer (Lead)</span>
          <span class="job-dates">July 2025 – Present</span>
        </div>
        <a class="job-company" href="https://www.themillionproject.org/" target="_blank">The Million Project, Germany (Remote)</a>
        <ul class="job-bullets">
          {format_bullets(bullets_million)}
        </ul>
      </article>

      <!-- JSES -->
      <article class="job-card">
        <div class="job-header">
          <span class="job-role">Machine Learning & Deep Learning Engineer</span>
          <span class="job-dates">July 2025 – Present</span>
        </div>
        <a class="job-company" href="https://bilijipub.com/" target="_blank">Journal of Sustainable Energy Systems, Ardabil, Iran</a>
        <ul class="job-bullets">
          {format_bullets(bullets_jses)}
        </ul>
      </article>

      <!-- Karlancer -->
      <article class="job-card">
        <div class="job-header">
          <span class="job-role">Freelance Full-Stack Developer</span>
          <span class="job-dates">May 2023 – March 2025</span>
        </div>
        <a class="job-company" href="https://www.karlancer.com/" target="_blank">Karlancer, Tehran, Iran</a>
        <ul class="job-bullets">
          {format_bullets(bullets_karlancer)}
        </ul>
      </article>

      <!-- Arman -->
      <article class="job-card">
        <div class="job-header">
          <span class="job-role">Frontend Developer</span>
          <span class="job-dates">May 2021 – May 2023</span>
        </div>
        <a class="job-company" href="#">ArmanPakhsheSahand, Ardabil, Iran</a>
        <ul class="job-bullets">
          {format_bullets(bullets_arman)}
        </ul>
      </article>
    </section>
  </main>

</body>
</html>
"""
    return html_content
