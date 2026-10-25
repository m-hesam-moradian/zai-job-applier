from pathlib import Path

file_path = Path("F:/talentflow-ai/src/tailor/cv_template.py")
content = file_path.read_text(encoding="utf-8").replace("\r\n", "\n")

# Add re import if not already present
if "import re" not in content:
    content = content.replace("from typing import Any", "import re\nfrom typing import Any")

helper_code = '''def _build_skill_categories_html(package: TailoredApplicationPackage | None) -> str:
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
        jd_keywords = {w for w in re.findall(r"[a-z0-9_\\-\\.+#]+", raw_text) if len(w) >= 2}

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
        html_blocks.append(f"""      <div class="skill-category">\\n        <div class="skill-cat-title">{cat_title}</div>\\n        <div class="skill-cat-body">{body_text}</div>\\n      </div>""")

    return "\\n\\n".join(html_blocks)
'''

# Find place to insert helper_code before render_cv_html
if "_build_skill_categories_html" not in content:
    content = content.replace("def render_cv_html(", helper_code + "\n\ndef render_cv_html(")

# Replace hardcoded skill categories in HTML
old_skills_html = '''      <div class="skill-category">
        <div class="skill-cat-title">SPOKEN LANGUAGES</div>
        <div class="skill-cat-body">English (B2/C1), German (A2/B1), Turkish (C1), Persian (C2)</div>
      </div>

      <div class="skill-category">
        <div class="skill-cat-title">PROGRAMMING LANGUAGES</div>
        <div class="skill-cat-body">JavaScript (ES6+), TypeScript, Python, C++, SQL, Solidity</div>
      </div>

      <div class="skill-category">
        <div class="skill-cat-title">FRONTEND DEVELOPMENT</div>
        <div class="skill-cat-body">React.js, Next.js, Tailwind CSS, ShadCN, Radix UI, MUI, Three.js, TanStack Query, Zod</div>
      </div>

      <div class="skill-category">
        <div class="skill-cat-title">BACKEND & APIS</div>
        <div class="skill-cat-body">Node.js, NestJS, Express.js, tRPC, Apollo GraphQL, RESTful APIs, IAM/SSO, OAuth2/JWT</div>
      </div>

      <div class="skill-category">
        <div class="skill-cat-title">DATABASES & ORM</div>
        <div class="skill-cat-body">Apache CouchDB, PostgreSQL, MySQL, MongoDB, Redis, Prisma ORM</div>
      </div>

      <div class="skill-category">
        <div class="skill-cat-title">AI & MACHINE LEARNING</div>
        <div class="skill-cat-body">PyTorch, TensorFlow, JAX, Transformers, LLMs (LoRA, RLHF, DPO), RAG, Vector DBs, LangGraph, LiteLLM</div>
      </div>

      <div class="skill-category">
        <div class="skill-cat-title">INFRASTRUCTURE & TOOLS</div>
        <div class="skill-cat-body">Docker, Docker Compose, Traefik, CI/CD, Git, pnpm Monorepos, Vitest, Linux/SSL</div>
      </div>'''

new_skills_html = "{skills_categories_html}"

if old_skills_html in content:
    content = content.replace(old_skills_html, new_skills_html)

# Add skills_categories_html variable assignment inside render_cv_html
if "skills_categories_html = _build_skill_categories_html(package)" not in content:
    content = content.replace(
        "    bullets_arman = [",
        "    skills_categories_html = _build_skill_categories_html(package)\n\n    bullets_arman = ["
    )

file_path.write_text(content, encoding="utf-8")
print("Successfully updated cv_template.py with dynamic category tailoring!")
