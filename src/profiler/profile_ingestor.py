"""GitHub + Resume Dynamic Profiler for TalentFlow-AI."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import httpx

from src.schemas.models import (
    DynamicCandidateProfile,
    DynamicTemplate,
    StaticIdentity,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Immutable seed data (Verified Ground Truth from LinkedIn + Official CV)
# ---------------------------------------------------------------------------

_STATIC_IDENTITY_SEED: dict[str, Any] = {
    "full_name": "Mohammad Hesam Moradian",
    "preferred_name": "Sam Moradian",
    "email": "m.hesam.moradian@gmail.com",
    "phone": "+18059007207",
    "location": "Ardabil Province, Iran (Targeting Relocation to Germany / Section 81a AufenthG Fast-Track & EU Blue Card)",
    "linkedin_url": "https://www.linkedin.com/in/m-hesam-moradian",
    "github_url": "https://github.com/m-hesam-moradian",
    "telegram_url": "https://t.me/sam_moradin1",
    "visa_status_summary": (
        "Fully eligible for the German Accelerated Skilled Worker Procedure (Section 81a AufenthG - fast-track visa within weeks) "
        "and EU Blue Card (B.Sc. in Computer Software Engineering with German Grade 1.5 'Sehr Gut' and H+ status in German Anabin database)."
    ),
    "languages": {
        "Persian": "Native (C2)",
        "Turkish": "Fluent (C1)",
        "English": "Fluent / Professional (B2/C1)",
        "German": "Proficient / Elementary (A2/B1)",
    },
    "education": [
        {
            "degree": "B.Sc. in Computer Software Engineering",
            "institution": "Islamic Azad University (IAU)",
            "dates": "Sep 2021 – May 2025",
            "location": "Ardabil, Iran",
            "academic_recognition": {
                "iran_grade": "18.5 / 20",
                "usa_gpa": "≈ 3.8 / 4.0",
                "german_grade": "1.5 (Sehr Gut)",
                "anabin_status": "H+ Recognized Institution and Degree",
            },
        },
        {
            "degree": "CS50x: Introduction to Computer Science",
            "institution": "Harvard University",
            "dates": "January 2024",
            "verification_id": "fe673d2f-6a44-46b6-8968-3d23f71c4c9f",
        },
    ],
    "certifications": [
        {
            "title": "CS50x: Introduction to Computer Science",
            "issuer": "Harvard University",
            "issued_date": "January 2024",
            "credential_id": "fe673d2f-6a44-46b6-8968-3d23f71c4c9f",
            "url": "https://cs50.harvard.edu/certificates/fe673d2f-6a44-46b6-8968-3d23f71c4c9f",
        }
    ],
    "work_history_anchors": [
        {
            "role_id": "role_million_project",
            "company": "The Million Project",
            "official_title": "Senior Full-Stack Engineer (Lead)",
            "dates": "July 2025 - Present",
            "location": "Germany (Remote / International)",
        },
        {
            "role_id": "role_jses",
            "company": "Journal of Sustainable Energy Systems",
            "official_title": "AI & Machine Learning Engineer",
            "dates": "August 2025 - Present",
            "location": "Ardabil, Iran (Research / Hybrid)",
        },
        {
            "role_id": "role_karlancer",
            "company": "Karlancer",
            "official_title": "Freelance Full-Stack Developer",
            "dates": "May 2023 - March 2025",
            "location": "Tehran / Ardabil, Iran",
        },
        {
            "role_id": "role_arman",
            "company": "ArmanAndish (Arman Pakhsh Sahand)",
            "official_title": "Frontend Developer",
            "dates": "May 2021 - May 2023",
            "location": "Ardabil, Iran",
        },
    ],
}

_CATEGORIZED_SKILLS_SEED: dict[str, list[str]] = {
    "Frontend Architecture": [
        "React",
        "Next.js",
        "TypeScript",
        "JavaScript",
        "Tailwind CSS",
        "Headless UI",
        "Radix UI",
        "Shadcn UI",
        "Material UI (MUI)",
        "Zustand",
        "TanStack Query",
        "Zod",
        "Three.js",
        "Vue.js",
        "HTML5",
        "CSS3",
        "Mobile-First UI",
        "Framer Motion",
    ],
    "Backend & APIs": [
        "Node.js",
        "Express.js",
        "NestJS",
        "FastAPI",
        "Python",
        "tRPC",
        "Apollo GraphQL",
        "RESTful API Design",
        "IAM / SSO",
        "OAuth2",
        "JWT",
        "Wix Velo",
        "Microservices",
    ],
    "Machine Learning & LLMOps": [
        "PyTorch",
        "TensorFlow",
        "JAX",
        "Transformers",
        "LLMOps",
        "Custom AI Agents",
        "RAG Infrastructure",
        "LangGraph",
        "LangChain",
        "LiteLLM",
        "Langfuse",
        "LoRA",
        "RLHF",
        "DPO",
        "Vector Databases",
        "SHAP",
        "LIME",
        "XGBoost",
        "LightGBM",
        "Scikit-learn",
        "Pandas",
        "NumPy",
        "CNNs",
        "LSTMs",
        "High Performance Computing (HPC)",
        "Distributed ML Training",
        "Model Evaluation Infra",
    ],
    "Databases & Caching": [
        "Apache CouchDB",
        "PostgreSQL",
        "MongoDB",
        "Redis",
        "MySQL",
        "Prisma ORM",
        "Vector DBs",
    ],
    "DevOps & Infrastructure": [
        "Docker",
        "Docker Compose",
        "Traefik v3.7",
        "CI/CD",
        "GitHub Actions",
        "Git",
        "Playwright",
        "Jest",
        "Vitest",
        "Cypress",
        "Pytest",
        "pnpm Monorepos",
        "Linux",
        "SSL / mkcert",
        "Cursor",
        "GitHub Copilot",
        "Prometheus",
        "Grafana",
        "W&B",
    ],
    "Web3 & Systems": [
        "Solidity",
        "Hardhat",
        "Smart Contracts",
        "C++",
        "Ethers.js",
        "IPFS",
    ],
}

# Flatten unique skills for fast ATS matching
_SKILL_BANK_FLAT: list[str] = sorted(
    {skill for cat in _CATEGORIZED_SKILLS_SEED.values() for skill in cat}
)

_DYNAMIC_TEMPLATE_SEED: dict[str, Any] = {
    "target_headline": "Senior Full-Stack AI Engineer | React, Node.js & Machine Learning Integration | Eligible for Fast-Track Visa (81a)",
    "executive_summary": (
        "Senior Full-Stack AI Engineer with over 4 years of proven experience unifying high-concurrency web platforms "
        "with production-grade machine learning pipelines, custom AI agents, and secure cloud infrastructure. Expert in architecting "
        "modular IAM/SSO microservices, type-safe API gateways (tRPC, GraphQL), and scalable Next.js/React frontends backed by Apache CouchDB, "
        "PostgreSQL, and Redis. Deeply skilled in statistical ML/DL pipelines (PyTorch, TensorFlow), distributed training, Explainable AI (SHAP, LIME), "
        "and production RAG systems. Certified by Harvard University (CS50x). Actively targeting relocation to Germany with full eligibility for "
        "the German Accelerated Skilled Worker Procedure (Section 81a AufenthG) and EU Blue Card (German Grade 1.5 'Sehr Gut' / Anabin H+)."
    ),
    "skill_bank": _SKILL_BANK_FLAT,
    "categorized_skills": _CATEGORIZED_SKILLS_SEED,
    "experience_bullets": {
        "role_million_project": [
            "Owned the complete software lifecycle for a high-concurrency social media MVP (Next.js 13.5 App Router, React 18, TypeScript, Tailwind CSS), delivering under tight deadlines.",
            "Architected custom, secure API layer using tRPC, Apollo GraphQL, and REST to enable multi-channel data flow between Next.js frontend and Wix Velo headless CMS / Apache CouchDB.",
            "Implemented strict authentication boundaries (IAM/SSO), JWT session management, automated testing with Vitest, and Docker CI/CD pipelines ensuring 99.9% uptime.",
            "Transitioned into Lead Developer role: recruited, mentored, and delegated architectural modules to junior developers to optimize system scalability and maintainability.",
        ],
        "role_jses": [
            "Architected and optimized end-to-end predictive ML/DL pipelines (XGBoost, LightGBM, Transformers via PyTorch/TensorFlow) for energy demand forecasting and sustainable systems.",
            "Hardened AI components by implementing advanced explainability (SHAP, LIME) and uncertainty calibration techniques (Monte Carlo simulations, Brier Score decompositions) for enterprise-grade decision-making.",
            "Structured complex machine learning models into secure, low-latency REST/FastAPI microservices for production deployment and business workflow integration.",
            "Engineered robust data balancing (SMOTE-ENC, CTAB-GAN), custom K-Fold Cross Validation, and metaheuristic optimizers to ensure model stability under varied data loads.",
        ],
        "role_karlancer": [
            "Architected and delivered scalable, high-performance web applications, including a production-ready full-stack e-commerce platform using React, Next.js, Node.js, and Express.js.",
            "Ensured strict end-to-end type safety using TypeScript and tRPC alongside client-side caching and state management via TanStack React Query.",
            "Designed secure RESTful APIs and optimized data persistence across MongoDB and SQL with JWT authentication and strict security boundaries.",
            "Spearheaded architectural overhaul and refactoring into clean architecture patterns and reusable UI components with Tailwind CSS and Material UI (MUI).",
        ],
        "role_arman": [
            "Engineered responsive, pixel-perfect user interfaces from scratch utilizing HTML5, modern CSS3, and vanilla JavaScript architectures.",
            "Spearheaded platform modernization by migrating legacy vanilla JavaScript codebase to a modern React and Tailwind CSS architecture.",
            "Designed scalable single-page application (SPA) component architecture leveraging custom React hooks, HOCs, and virtual DOM optimization.",
        ],
    },
    "project_bank": [
        {
            "name": "Block-MLA",
            "tech_stack": ["Python", "PyTorch", "FastAPI", "Distributed Training", "MLOps", "Redis", "PostgreSQL", "Prometheus", "Grafana", "Docker"],
            "description": "Dynamic Tensor-Aware Momentum Look-Ahead — 20-Node asynchronous distributed ML training system featuring a novel outer optimizer (BlockMLAOptimizer) with per-block cosine-gated momentum, NanoGPT 60M, and full MLOps monitoring stack.",
            "url": "https://github.com/m-hesam-moradian/Block-MLA",
        },
        {
            "name": "talentflow-ai",
            "tech_stack": ["Python", "LangGraph", "LiteLLM", "Playwright", "FastAPI", "ReportLab", "Pydantic", "Docker"],
            "description": "Autonomous Agentic Career & Document Orchestrator for the German Tech Market — multi-agent system profiling candidates from live GitHub metadata, filtering visa-eligible jobs, dynamically tailoring ATS CVs and motivation letters, and applying via Playwright multi-tab browser automation.",
            "url": "https://github.com/m-hesam-moradian/talentflow-ai",
        },
        {
            "name": "techaxon-auth",
            "tech_stack": ["Traefik v3.7", "NestJS", "Next.js", "Apache CouchDB", "Redis", "Docker Compose", "mkcert", "pnpm", "JWT"],
            "description": "Production-grade local infrastructure and IAM service with Traefik reverse proxy, automatic local HTTPS certificate provisioning via mkcert, CouchDB/Redis persistence, and NestJS Identity Provider microservice.",
            "url": "https://github.com/m-hesam-moradian/techaxon-auth",
        },
        {
            "name": "theMillionProject-feeds",
            "tech_stack": ["Next.js 13.5", "React 18", "TypeScript", "Tailwind CSS", "Wix Velo", "Zustand", "Jest", "Cypress", "Vercel"],
            "description": "Scalable full-stack social media feeds platform built with Next.js App Router and Wix Headless CMS backend, featuring infinite scrolling feeds, real-time sync via Data Hooks, and comprehensive UML design.",
            "url": "https://github.com/m-hesam-moradian/theMillionProject-feeds-fullStack-Next.js",
        },
        {
            "name": "lms-project",
            "tech_stack": ["Next.js", "TypeScript", "Apache CouchDB", "Apollo GraphQL", "tRPC", "REST API", "Docker", "Zod", "Tailwind CSS"],
            "description": "Modular Learner Management System featuring unified API layer with Apollo GraphQL and tRPC, CouchDB document storage, automated code generation, and responsive dark-theme admin dashboard.",
            "url": "https://github.com/m-hesam-moradian/lms-project",
        },
        {
            "name": "Prescriptive Analytics Research",
            "tech_stack": ["Python", "PyTorch", "XGBoost", "Scikit-learn", "SHAP", "LIME", "LightGBM"],
            "description": "Experimental deep learning & prescriptive analytics research pipeline combining XGBoost, Transformers, and causal inference for energy demand forecasting at JSES.",
            "url": "https://github.com/m-hesam-moradian",
        },
        {
            "name": "TEMPO",
            "tech_stack": ["React", "TypeScript", "PWA", "IndexedDB", "Tailwind CSS"],
            "description": "Standalone Progressive Web Application (PWA) for workout coaching and real-time set tracking with offline IndexedDB support.",
            "url": "https://github.com/m-hesam-moradian/TEMPO",
        },
        {
            "name": "NFT-marketPlace",
            "tech_stack": ["Next.js", "Hardhat", "Solidity", "Ethers.js", "IPFS"],
            "description": "Decentralized digital asset marketplace engineered with Hardhat smart contracts, Next.js frontend, and IPFS metadata storage.",
            "url": "https://github.com/m-hesam-moradian/NFT-marketPlace",
        },
        {
            "name": "Bigbind",
            "tech_stack": ["Python", "Blockchain", "Proof of Useful Work", "FastAPI"],
            "description": "Decentralized AI ecosystem architecture utilizing multi-layered blockchain structures and Proof of Useful Work consensus for distributed ML training rewards.",
            "url": "https://github.com/m-hesam-moradian/Bigbind",
        },
    ],
}


def _fetch_github_repos(github_username: str) -> list[dict[str, Any]]:
    """Fetch repos from GitHub API with graceful offline fallback."""
    url = f"https://api.github.com/users/{github_username}/repos?sort=updated&per_page=30"
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(url, headers={"Accept": "application/vnd.github.v3+json"})
            if response.status_code == 200:
                return response.json()
            logger.warning("GitHub API returned %s — using seed data only.", response.status_code)
    except Exception as exc:
        logger.warning("GitHub API unreachable (%s) — using seed data only.", exc)
    return []


def _merge_github_repos(
    project_bank: list[dict[str, Any]],
    github_repos: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Enrich seed projects with live GitHub metadata; add any new repos found."""
    seed_names_lower = {p["name"].lower(): p for p in project_bank}
    merged = [p.copy() for p in project_bank]

    for repo in github_repos:
        name = repo.get("name", "")
        description = repo.get("description") or ""
        html_url = repo.get("html_url", "")
        language = repo.get("language") or ""

        key = name.lower()
        if key in seed_names_lower:
            proj = seed_names_lower[key]
            if not proj.get("description") and description:
                proj["description"] = description
            if html_url and not proj.get("url"):
                proj["url"] = html_url
        else:
            merged.append(
                {
                    "name": name,
                    "tech_stack": [language] if language else [],
                    "description": description,
                    "url": html_url,
                }
            )

    return merged


def build_dynamic_profile(
    github_username: str = "m-hesam-moradian",
    output_path: Path = Path("data/dynamic_profile.json"),
) -> DynamicCandidateProfile:
    """Build and persist a DynamicCandidateProfile from GitHub + seed data."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Fetch live GitHub repos (falls back silently if offline / rate-limited)
    github_repos = _fetch_github_repos(github_username)

    # Enrich project_bank with live GitHub data
    enriched_projects = _merge_github_repos(
        _DYNAMIC_TEMPLATE_SEED["project_bank"],
        github_repos,
    )

    dynamic_template_data = {**_DYNAMIC_TEMPLATE_SEED, "project_bank": enriched_projects}

    profile = DynamicCandidateProfile(
        static_identity=StaticIdentity(**_STATIC_IDENTITY_SEED),
        dynamic_template=DynamicTemplate(**dynamic_template_data),
    )

    # Write to disk
    profile_json = profile.model_dump(mode="json")
    json_str = json.dumps(profile_json, indent=2, ensure_ascii=False)

    output_path.write_text(json_str, encoding="utf-8")
    logger.info("Dynamic profile written to %s", output_path)

    # Also write master_resume.json
    master_path = output_path.parent / "master_resume.json"
    master_path.write_text(json_str, encoding="utf-8")
    logger.info("Master resume written to %s", master_path)

    # Also write ultimate_profile.json
    ultimate_path = output_path.parent / "ultimate_profile.json"
    ultimate_path.write_text(json_str, encoding="utf-8")
    logger.info("Ultimate profile written to %s", ultimate_path)

    return profile
