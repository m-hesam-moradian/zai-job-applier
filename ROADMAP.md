# TalentFlow-AI — Roadmap

## ✅ Phase 0: Foundation
- [x] Project structure and `pyproject.toml`
- [x] `src/config.py` and `tests/test_config.py`

## ✅ Phase 1: Core Modules (AUTOBUILD Steps 1-7)
- [x] **Step 1:** Master Architecture Spec (`AUTOBUILD.md`) & Pydantic v2 schemas (`src/schemas/models.py`)
  - `StaticIdentity` (immutable candidate identity)
  - `DynamicTemplate` (mutable per-job CV template slots)
  - `DynamicCandidateProfile`
  - `JobPosting` with 16-column `.to_sheet_row()` export
  - `TailoredApplicationPackage`
- [x] **Step 2:** Live GitHub + Resume Extractor (`src/profiler/profile_ingestor.py`)
  - Live GitHub API query with 5-second timeout & graceful offline fallback
  - Seed static identity with Mohammad Hesam Moradian's verified background
  - Generated `data/dynamic_profile.json` & `data/master_resume.json`
- [x] **Step 3:** Visa Sponsorship & ATS Filter (`src/ingestion/visa_filter.py`)
  - Hard blockers rejection (`arbeitserlaubnis für deutschland erforderlich`, `eu citizenship required`, `only eu citizens`, `no visa sponsorship`, `c2 german required`)
  - Non-engineering roles exclusion unless high-priority source
  - Priority boost (+25) for explicit visa sponsorship / EU Blue Card
  - Standard boost (+10) for qualifying software/ML engineering roles
- [x] **Step 4:** Dynamic ATS CV + Motivation Letter PDF Engine (`src/tailor/document_tailor.py`)
  - Keyword matching & ranking engine (LiteLLM + deterministic fallback)
  - Deterministic Anti-Hallucination Guardrail (strips unsupported skills)
  - PDF generation (`Moradian_Hesam_CV.pdf` & `Moradian_Hesam_Motivation_Letter.pdf`)
- [x] **Step 5:** Multi-Tab Human-Handoff Playwright Browser (`src/browser_bot/multi_tab_applier.py`)
  - Shared single browser context across job queue
  - New tab per application with auto-fill & file upload
  - Human-Action Detector for CAPTCHA, login walls, and unfilled required fields
  - Floating high-contrast banner injection and non-blocking human-handoff tabs
- [x] **Step 6:** Unified CLI & Sample Jobs (`src/auto_agent.py` & `data/sample_jobs.json`)
  - `--init-profile` CLI flag
  - `--jobs-file` pipeline flag with `--headless` and `--auto-submit`
  - Run summary generation (`output/run_summary.json`)
- [x] **Step 7:** Automated Verification & Testing
  - 10/10 automated tests passing in `tests/test_autobuild_e2e.py` and `tests/test_config.py`
  - 100% clean linter checks with `ruff check` (0 errors)

## 🔜 Phase 2: Next Steps
- [ ] Scraping integration using Antigravity browser tools
- [ ] Multi-agent orchestration with LangGraph
- [ ] Observability with Langfuse
- [ ] Google Sheets integration for synchronized live application tracking
