"""End-to-end automated tests for TalentFlow-AI."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.schemas.models import (
    DynamicCandidateProfile,
    JobPosting,
)

# ---------------------------------------------------------------------------
# Test 1: Dynamic Profile Builder
# ---------------------------------------------------------------------------


def test_dynamic_profile_builder(tmp_path: Path) -> None:
    """Verify build_dynamic_profile creates valid profile with immutable static_identity."""
    from src.profiler.profile_ingestor import build_dynamic_profile

    output_path = tmp_path / "dynamic_profile.json"
    profile = build_dynamic_profile(github_username="m-hesam-moradian", output_path=output_path)

    assert isinstance(profile, DynamicCandidateProfile)
    si = profile.static_identity

    # Immutable identity checks
    assert si.full_name == "Mohammad Hesam Moradian"
    assert si.email == "m.hesam.moradian@gmail.com"
    assert si.phone in ["+18059007207", "+98-912-000-0000"]
    assert "Germany" in si.location
    assert si.linkedin_url == "https://www.linkedin.com/in/m-hesam-moradian"
    assert si.github_url == "https://github.com/m-hesam-moradian"
    assert len(si.education) >= 2
    assert len(si.work_history_anchors) >= 3

    # Dynamic template checks
    dt = profile.dynamic_template
    assert "Python" in dt.skill_bank
    assert len(dt.skill_bank) >= 10
    assert len(dt.project_bank) >= 5
    assert "role_million_project" in dt.experience_bullets
    assert "role_jses" in dt.experience_bullets

    # Output file check
    assert output_path.exists()
    loaded = json.loads(output_path.read_text(encoding="utf-8"))
    assert loaded["static_identity"]["full_name"] == "Mohammad Hesam Moradian"


# ---------------------------------------------------------------------------
# Test 2: Visa Sponsorship Gatekeeper
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "job_data,expected_eligible",
    [
        # Should PASS — explicit visa sponsorship
        (
            {
                "id": "j1",
                "title": "Senior AI Engineer",
                "company": "TestCo",
                "location": "Berlin, Germany",
                "description": "We provide visa sponsorship and relocation support for EU Blue Card.",
                "visa_status": "sponsorship available",
            },
            True,
        ),
        # Should PASS — standard engineering role
        (
            {
                "id": "j2",
                "title": "Machine Learning Engineer",
                "company": "TestCo2",
                "location": "Munich, Germany",
                "description": "Build ML pipelines with PyTorch and FastAPI.",
                "visa_status": "",
            },
            True,
        ),
        # Should FAIL — no visa sponsorship
        (
            {
                "id": "j3",
                "title": "Senior Software Engineer",
                "company": "LocalCorp",
                "location": "Berlin, Germany",
                "description": "No visa sponsorship. Native-level German proficiency is required (C2).",
                "visa_status": "",
            },
            False,
        ),
        # Should FAIL — EU citizenship required
        (
            {
                "id": "j4",
                "title": "Backend Developer",
                "company": "EUCorp",
                "location": "Frankfurt",
                "description": "EU citizenship required for this position.",
                "visa_status": "",
            },
            False,
        ),
        # Should FAIL — non-engineering role (product manager)
        (
            {
                "id": "j5",
                "title": "Product Manager AI",
                "company": "TestCo3",
                "location": "Hamburg",
                "description": "Great ML environment, relocation support offered.",
                "visa_status": "sponsorship available",
            },
            False,
        ),
        # Should FAIL — working student
        (
            {
                "id": "j6",
                "title": "Working Student Software Engineering",
                "company": "TestCo4",
                "location": "Berlin",
                "description": "Part-time working student position.",
                "visa_status": "",
            },
            False,
        ),
    ],
)
def test_visa_sponsorship_gatekeeper(job_data: dict, expected_eligible: bool) -> None:
    """Verify visa gatekeeper correctly filters jobs."""
    from src.ingestion.visa_filter import evaluate_visa_and_role_eligibility

    job = JobPosting(**job_data)
    is_eligible, reason, boost = evaluate_visa_and_role_eligibility(job)
    assert is_eligible == expected_eligible, (
        f"Job '{job.title}': expected {expected_eligible}, got {is_eligible}. Reason: {reason}"
    )


# ---------------------------------------------------------------------------
# Test 3: Dynamic CV + Motivation Letter PDFs
# ---------------------------------------------------------------------------


def test_dynamic_cv_and_motivation_letter_pdfs(tmp_path: Path) -> None:
    """Verify tailoring strips hallucinated skills and compiles valid PDFs."""
    from src.profiler.profile_ingestor import build_dynamic_profile
    from src.tailor.document_tailor import compile_application_pdfs, tailor_application_for_job

    profile = build_dynamic_profile(
        github_username="m-hesam-moradian",
        output_path=tmp_path / "profile.json",
    )

    job = JobPosting(
        id="test_job_001",
        title="Senior Full-Stack Engineer",
        company="TestGmbH",
        location="Berlin, Germany",
        description=(
            "We need Python, FastAPI, React, Next.js, LangGraph, Docker expertise. "
            "We also require COBOL and Rust experience. Visa sponsorship available."
        ),
        visa_status="sponsorship available",
    )

    package = tailor_application_for_job(job, profile)

    # Anti-hallucination guardrail: COBOL and Rust must be stripped
    assert "COBOL" not in package.selected_skills, (
        "COBOL should be stripped by anti-hallucination guardrail"
    )
    assert "Rust" not in package.selected_skills, (
        "Rust should be stripped by anti-hallucination guardrail"
    )

    # JD keywords should be prioritized
    assert "Python" in package.selected_skills[:5], "Python should be near top since it's in JD"

    # Motivation letter must be non-empty and mention the company
    assert len(package.motivation_letter) > 100, "Motivation letter should be substantial"
    assert "TestGmbH" in package.motivation_letter, "Motivation letter must mention the company"

    # Compile PDFs
    pdf_paths = compile_application_pdfs(package, profile, tmp_path)
    cv_path = pdf_paths["cv_pdf"]
    ml_path = pdf_paths["motivation_pdf"]

    # Verify PDF files exist and are valid PDFs
    assert cv_path.exists(), "CV PDF must exist"
    assert ml_path.exists(), "Motivation Letter PDF must exist"

    with open(cv_path, "rb") as f:
        header = f.read(4)
    assert header == b"%PDF", f"CV PDF must start with %PDF, got {header!r}"

    with open(ml_path, "rb") as f:
        header = f.read(4)
    assert header == b"%PDF", f"Motivation Letter PDF must start with %PDF, got {header!r}"

    # Static identity must not be altered
    si = profile.static_identity
    assert si.full_name == "Mohammad Hesam Moradian"
    assert si.email == "m.hesam.moradian@gmail.com"
    for anchor in si.work_history_anchors:
        assert anchor["company"] in [
            "The Million Project",
            "Journal of Sustainable Energy Systems",
            "Independent / Freelance",
            "Karlancer",
            "ArmanAndish (Arman Pakhsh Sahand)",
        ]


# ---------------------------------------------------------------------------
# Test 4: Multi-Tab Browser Applier
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_multi_tab_applier_submits_clean_and_keeps_human_blocker_tab_open(
    tmp_path: Path,
) -> None:
    """Test multi-tab browser: clean form auto-submits, captcha form stays open."""
    from src.browser_bot.multi_tab_applier import MultiTabBrowserApplier
    from src.profiler.profile_ingestor import build_dynamic_profile
    from src.tailor.document_tailor import compile_application_pdfs, tailor_application_for_job

    # Create mock HTML pages
    job1_html = tmp_path / "job1_clean.html"
    job1_html.write_text(
        """<!DOCTYPE html><html><body>
        <form id="apply-form">
            <input type="text" name="firstname" placeholder="First Name" />
            <input type="text" name="lastname" placeholder="Last Name" />
            <input type="email" name="email" placeholder="Email" />
            <input type="file" name="resume" />
            <textarea name="cover_letter" placeholder="Cover Letter"></textarea>
            <button type="submit">Submit Application</button>
        </form>
        </body></html>""",
        encoding="utf-8",
    )

    job2_html = tmp_path / "job2_captcha.html"
    job2_html.write_text(
        """<!DOCTYPE html><html><body>
        <form id="apply-form">
            <input type="text" name="firstname" placeholder="First Name" />
            <input type="email" name="email" placeholder="Email" />
            <input type="file" name="resume" />
            <textarea name="cover_letter" placeholder="Cover Letter"></textarea>
            <div id="captcha" class="g-recaptcha" data-human-required="true"></div>
            <button type="submit">Submit Application</button>
        </form>
        </body></html>""",
        encoding="utf-8",
    )

    job3_html = tmp_path / "job3_clean.html"
    job3_html.write_text(
        """<!DOCTYPE html><html><body>
        <form id="apply-form">
            <input type="text" name="name" placeholder="Full Name" />
            <input type="email" name="email" placeholder="Email" />
            <input type="file" name="resume" />
            <textarea name="cover_letter" placeholder="Cover Letter"></textarea>
            <button type="submit">Submit</button>
        </form>
        </body></html>""",
        encoding="utf-8",
    )

    # Build profile and create packages
    profile = build_dynamic_profile(
        github_username="m-hesam-moradian",
        output_path=tmp_path / "profile.json",
    )

    jobs = [
        JobPosting(
            id="t001",
            title="Senior Engineer",
            company="CleanCo",
            location="Berlin",
            description="Python FastAPI React",
            url=job1_html.as_uri(),
        ),
        JobPosting(
            id="t002",
            title="ML Engineer",
            company="CaptchaCo",
            location="Munich",
            description="PyTorch MLOps",
            url=job2_html.as_uri(),
        ),
        JobPosting(
            id="t003",
            title="Full-Stack Engineer",
            company="CleanCo2",
            location="Hamburg",
            description="Next.js TypeScript",
            url=job3_html.as_uri(),
        ),
    ]

    packages_and_paths = []
    for job in jobs:
        package = tailor_application_for_job(job, profile)
        pdf_paths = compile_application_pdfs(package, profile, tmp_path)
        packages_and_paths.append(
            (job, package, pdf_paths.get("cv_pdf"), pdf_paths.get("motivation_pdf"))
        )

    # Run applier with auto_submit=True but keep_open_on_blocker=True (default)
    applier = MultiTabBrowserApplier(
        output_dir=tmp_path / "output",
        headless=True,
        auto_submit=True,
        keep_open_on_blocker=True,
    )

    results = await applier.apply_batch(packages_and_paths)

    assert len(results) == 3

    # Job 1 (clean) — should be SUBMITTED
    r1 = next(r for r in results if r["job_id"] == "t001")
    assert r1["status"] == "SUBMITTED", f"Expected SUBMITTED, got {r1['status']}"

    # Job 2 (captcha) — should be OPEN_IN_TAB_NEEDS_HUMAN
    r2 = next(r for r in results if r["job_id"] == "t002")
    assert r2["status"] == "OPEN_IN_TAB_NEEDS_HUMAN", (
        f"Expected OPEN_IN_TAB_NEEDS_HUMAN, got {r2['status']}"
    )

    # Job 3 (clean) — should be SUBMITTED
    r3 = next(r for r in results if r["job_id"] == "t003")
    assert r3["status"] == "SUBMITTED", f"Expected SUBMITTED, got {r3['status']}"
