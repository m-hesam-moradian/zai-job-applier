# TalentFlow-AI — Master Architecture Specification

## Overview
TalentFlow-AI is a fully autonomous AI career and job-application orchestration system.

## 5-Module Architecture

### Module 1: GitHub + Resume Dynamic Profiler
- Queries GitHub API for real repo metadata (names, descriptions, languages, URLs).
- Merges live data with immutable seed static identity.
- Outputs `data/dynamic_profile.json` and `data/master_resume.json`.

### Module 2: Visa Sponsorship Gatekeeper
- Hard-blocks EU-citizenship-required, no-sponsorship, C2-German, and non-engineering roles.
- Priority boost for explicit visa/Blue Card sponsors (+25).
- Standard boost for qualifying DE/EU engineering roles (+10).

### Module 3: Dynamic ATS CV + Motivation Letter PDF Engine
- LiteLLM-powered tailoring with offline deterministic keyword-ranking fallback.
- Anti-hallucination guardrail: strips skills not in candidate's skill_bank.
- Generates two A4 PDFs per job: CV and Motivation Letter.

### Module 4: Multi-Tab Human-Handoff Playwright Browser
- Single browser context, one new tab per job.
- Auto-fills fields and uploads PDFs.
- Detects CAPTCHA/login/unfilled-required fields; injects warning banner and keeps tab open for human completion.

### Module 5: Unified CLI & CI/CD
- `--init-profile`: builds dynamic profile from GitHub + seed data.
- `--jobs-file`: filters, tailors, compiles PDFs, and runs browser applier for all eligible jobs.
- Outputs `output/run_summary.json`.
