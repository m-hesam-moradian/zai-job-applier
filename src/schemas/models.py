"""Pydantic v2 data models for TalentFlow-AI."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, model_validator


class StaticIdentity(BaseModel):
    """Immutable candidate identity — never modified by LLM."""

    full_name: str
    preferred_name: str = "Sam Moradian"
    email: str
    phone: str
    location: str
    linkedin_url: str
    github_url: str
    telegram_url: str = "https://t.me/sam_moradin1"
    visa_status_summary: str = (
        "Eligible for German Accelerated Skilled Worker Procedure (Section 81a AufenthG) "
        "and EU Blue Card (German Grade 1.5 / Anabin H+ Recognized Degree)"
    )
    languages: dict[str, str] | list[str]
    education: list[dict[str, Any]]
    certifications: list[dict[str, Any]] = Field(default_factory=list)
    work_history_anchors: list[dict[str, Any]]


class DynamicTemplate(BaseModel):
    """Mutable per-job CV template slots."""

    target_headline: str = ""
    executive_summary: str = ""
    skill_bank: list[str] = Field(default_factory=list)
    categorized_skills: dict[str, list[str]] = Field(default_factory=dict)
    experience_bullets: dict[str, list[str]] = Field(default_factory=dict)
    project_bank: list[dict[str, Any]] = Field(default_factory=list)


class DynamicCandidateProfile(BaseModel):
    """Full candidate profile combining static identity and dynamic template."""

    static_identity: StaticIdentity
    dynamic_template: DynamicTemplate


class JobPosting(BaseModel):
    """A single job posting scraped or loaded from a source."""

    id: str
    source: str = ""
    title: str
    company: str
    location: str
    work_mode: str = ""
    visa_status: str = ""
    url: str = ""
    description: str = ""
    posted_at: str = ""

    @model_validator(mode="before")
    @classmethod
    def _normalize_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Normalize ID
            if "id" not in data and "jobId" in data:
                data["id"] = str(data["jobId"])
            elif "id" not in data:
                data["id"] = "job_unknown"

            # Normalize URL
            if not data.get("url"):
                data["url"] = data.get("applyUrl") or data.get("linkedinUrl") or ""

            # Normalize posted_at
            if not data.get("posted_at"):
                data["posted_at"] = data.get("savedAt") or ""

            # Normalize source
            if not data.get("source"):
                data["source"] = data.get("companyInfo") or ""

            # Clean inverted title / company if present from LinkedIn scraping
            raw_title = data.get("title", "")
            raw_comp = data.get("company", "")
            if "·" in raw_title and any(
                kw in raw_comp.lower()
                for kw in ["engineer", "developer", "fde", "architect", "lead"]
            ):
                data["title"] = raw_comp.replace("(Save)", "").strip()
                data["company"] = raw_title.split("·")[0].strip()

        return data

    def to_sheet_row(self) -> list[Any]:
        """Return a 16-column list for spreadsheet export."""
        return [
            self.id,
            self.source,
            self.title,
            self.company,
            self.location,
            self.work_mode,
            self.visa_status,
            self.url,
            self.description[:200] if self.description else "",
            self.posted_at,
            "",  # col 11: match_score placeholder
            "",  # col 12: visa_eligible placeholder
            "",  # col 13: visa_reason placeholder
            "",  # col 14: tailored_headline placeholder
            "",  # col 15: status placeholder
            "",  # col 16: notes placeholder
        ]


class TailoredApplicationPackage(BaseModel):
    """Result of tailoring a job application for a specific posting."""

    job_id: str
    company: str
    job_title: str
    match_score: int = Field(ge=0, le=100)
    visa_eligible: bool
    visa_reason: str = ""
    tailored_headline: str = ""
    tailored_summary: str = ""
    selected_skills: list[str] = Field(default_factory=list)
    tailored_bullets: dict[str, list[str]] = Field(default_factory=dict)
    selected_projects: list[dict[str, Any]] = Field(default_factory=list)
    motivation_letter: str = ""
    hallucinations_stripped: list[str] = Field(default_factory=list)
