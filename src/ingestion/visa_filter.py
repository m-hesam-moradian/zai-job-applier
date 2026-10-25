"""Visa Sponsorship & ATS Role Eligibility Filter for TalentFlow-AI."""
from __future__ import annotations

import re

from src.schemas.models import JobPosting

# ---------------------------------------------------------------------------
# Hard blockers — any match → immediate rejection
# ---------------------------------------------------------------------------
_HARD_BLOCKERS: list[str] = [
    "arbeitserlaubnis für deutschland erforderlich",
    "arbeitserlaubnis in deutschland",
    "eu citizenship required",
    "only eu citizens",
    "no visa sponsorship",
    "keine visumsunterstützung",
    "c2 german required",
    "native-level german proficiency is required",
    "deutsch verhandlungssicher (c2)",
    "fließend deutsch in wort und schrift",
    "verhandlungssichere deutschkenntnisse (c1/c2)",
]

# Non-engineering role keywords → reject unless HIGH PRIORITY source
_NON_ENGINEERING_ROLES: list[str] = [
    "product manager",
    "public affairs",
    r"\bsales\b",
    "recruiter",
    r"\bhr\b",
    "marketing",
    "working student",
    "praktikum",
    "werkstudent",
    r"\bintern\b",
]

# Incompatible language / tech stack keywords in title
_INCOMPATIBLE_STACK_PATTERNS: list[str] = [
    r"\bjava\b",
    r"\bc#\b",
    r"\b\.net\b",
    r"\bphp\b",
    r"\bruby\b",
    r"\bios\b",
    r"\bandroid\b",
    r"\bswift\b",
    r"\bkotlin\b",
    r"\bsalesforce\b",
    r"\bsap\b",
    r"\bcobol\b",
    r"\bscala\b",
]

# Visa / relocation sponsorship signals → Top Priority Boost (+30)
_VISA_SIGNALS: list[str] = [
    "visa sponsorship",
    "visa-sponsorship",
    "relocation support",
    "eu blue card",
    "blaue karte",
    "relocation package",
    "sponsorship available",
    "relocation assistance",
    "visa-unterstützung",
    "visumsunterstützung",
    "section 81a",
    "beschleunigtes fachkräfteverfahren",
    "sponsor visa",
    "sponsoring visa",
]

# Remote work signals → Second Priority Boost (+20)
_REMOTE_SIGNALS: list[str] = [
    "remote",
    "home office",
    "home-office",
    "work from home",
    "telearbeit",
    "fully remote",
    "100% remote",
    "work from anywhere",
]


def _text_lower(*fields: str) -> str:
    """Concatenate and lowercase all provided text fields."""
    return " ".join(f for f in fields if f).lower()


def evaluate_visa_and_role_eligibility(
    job: JobPosting,
    strict_visa_or_remote: bool = False,
) -> tuple[bool, str, int]:
    """Evaluate whether a job is eligible and compute prioritized score.

    Priority Ranking:
    1. Visa Sponsorship + Remote (+50 boost) - Ultra Priority
    2. Visa Sponsorship (+30 boost) - Top Priority
    3. Remote Work (+20 boost) - Second Priority
    4. Standard Qualifying Engineering Role (+10 boost)

    Args:
        job: The job posting to evaluate.
        strict_visa_or_remote: If True, strictly requires either explicit visa sponsorship
            or remote work option; on-site jobs without sponsorship are rejected.

    Returns:
        (is_eligible: bool, reason: str, priority_boost: int)
    """
    description_lower = _text_lower(job.description, job.visa_status)
    title_lower = job.title.lower()
    work_mode_lower = _text_lower(job.work_mode, job.location, job.description)
    is_high_priority = job.source.startswith("0 - HIGH PRIORITY")

    # 1. Hard blockers check
    for blocker in _HARD_BLOCKERS:
        if blocker in description_lower:
            return False, f"Hard blocker matched: '{blocker}'", 0

    # 2. Non-engineering role filter
    if not is_high_priority:
        for pattern in _NON_ENGINEERING_ROLES:
            if re.search(pattern, title_lower):
                return (
                    False,
                    f"Non-engineering role pattern matched in title: '{pattern}'",
                    0,
                )

    # 3. Incompatible tech stack filter (e.g. Java, C#, PHP, Swift in title)
    for pattern in _INCOMPATIBLE_STACK_PATTERNS:
        if re.search(pattern, title_lower):
            return (
                False,
                f"Incompatible technology stack in title: '{pattern}'",
                0,
            )

    # 4. Check Priority Signals
    has_visa_sponsorship = any(sig in description_lower for sig in _VISA_SIGNALS)
    has_remote_option = any(sig in work_mode_lower for sig in _REMOTE_SIGNALS)

    boost = 0
    reasons: list[str] = []

    # Priority 1: Visa Sponsorship (+30)
    if has_visa_sponsorship:
        boost += 30
        reasons.append("Visa Sponsorship / Relocation / Blue Card detected (+30)")

    # Priority 2: Remote Work (+20)
    if has_remote_option:
        boost += 20
        reasons.append("Remote work option detected (+20)")

    if boost > 0:
        return True, " | ".join(reasons), boost

    # 5. Strict mode check: Must have visa sponsorship OR remote
    if strict_visa_or_remote:
        return (
            False,
            "Strict mode: On-site / hybrid role without explicit visa sponsorship or remote option.",
            0,
        )

    # 6. Standard engineering pass (+10)
    engineering_keywords = [
        "engineer",
        "developer",
        "software",
        "machine learning",
        "data scientist",
        "fullstack",
        "full-stack",
        "backend",
        "frontend",
        "devops",
        "mlops",
        "ai ",
        "ml ",
        "fde",
    ]
    for kw in engineering_keywords:
        if kw in title_lower:
            return (
                True,
                "Qualifying engineering role without explicit visa blocker (German Fast-Track / Blue Card eligible).",
                10,
            )

    return (
        True,
        "No blockers found; eligible by default.",
        0,
    )
