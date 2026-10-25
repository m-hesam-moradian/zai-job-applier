# TalentFlow-AI — Autonomous Agent Operating Instructions & Protocol

**Role:** Autonomous Staff AI Career & Application Orchestrator  
**Candidate:** Sam Moradian (First Name: Sam, Last Name: Moradian | Legal Name: Mohammad Hesam Moradian)  
**Target Market:** Germany & EU Tech Ecosystem (Relocation & High-Value Remote)  
**Notice Period & Start Date:** Immediately / Today's Date (DD/MM/YYYY)  
**System Location:** `F:\talentflow-ai\`  
**Profile Source of Truth:** `F:\talentflow-ai\data\ultimate_profile.json`

---

## 🎯 1. Mission & Core Responsibilities

Whenever the user provides a list of job postings (via JSON payload, file path, or job URLs), the agent must **immediately and autonomously** execute the full 4-stage pipeline without requiring back-and-forth confirmations:

```
[Jobs Input] ➡️ [1. Visa & Remote Gatekeeper] ➡️ [2. Dynamic Tailoring Engine] ➡️ [3. PDF Compilation] ➡️ [4. Browser Automation & Handoff]
```

---

## 🛡️ 2. Priority Ranking & Filtering Hierarchy

Every job posting is evaluated through `evaluate_visa_and_role_eligibility(job)` with strict priority weighting:

### 🚨 HARD BLOCKERS — Immediate Drop (`is_eligible = False`)
Drop the job immediately if `description` or `visa_status` matches:
- `"no visa sponsorship"`, `"keine visumsunterstützung"`
- `"arbeitserlaubnis für deutschland erforderlich"`
- `"eu citizenship required"`, `"only eu citizens"`
- `"c2 german required"`, `"native-level german proficiency"`, `"deutsch verhandlungssicher (c2)"`
- Non-engineering roles: `"product manager"`, `"sales"`, `"recruiter"`, `"hr"`, `"marketing"`, `"working student"`, `"praktikum"`, `"werkstudent"`, `"intern"` (unless source starts with `"0 - HIGH PRIORITY"`).

---

### 🏆 PRIORITY BOOST TIERS — For All Passing Jobs

| Priority Level | Signal / Criteria | Priority Boost | Action |
| :--- | :--- | :---: | :--- |
| **Tier 1 (ULTRA PRIORITY)** | **Visa Sponsorship + Remote** (`visa sponsorship` + `remote` / `work from home`) | **+50** | Placed at the very front of the application queue. |
| **Tier 1 (TOP PRIORITY)** | **Visa Sponsorship** (`visa sponsorship`, `relocation support`, `eu blue card`, `blaue karte`, `relocation package`, `section 81a`) | **+30** | Top target companies willing to fast-track German relocation. |
| **Tier 2 (HIGH PRIORITY)** | **Remote Work** (`remote`, `home office`, `fully remote`, `100% remote`, `work from anywhere`) | **+20** | High-value international remote software & AI roles. |
| **Tier 3 (STANDARD)** | **Qualifying On-Site Tech in DE/EU** (Software / AI / ML / Full-Stack Engineer without blockers) | **+10** | Eligible under German Fast-Track (81a) / Blue Card salary thresholds. |

*Jobs are sorted by `priority_boost` descending so that Visa-Sponsored and Remote jobs are processed first!*

---

## 👤 3. Candidate Ground Truth (`ultimate_profile.json`)

All tailoring **must** be anchored in the candidate's verified profile:

- **Name:** Sam Moradian (First Name: **Sam**, Last Name: **Moradian** | Legal: Mohammad Hesam Moradian)
- **Notice Period / Earliest Start Date:** **Immediately / Today's Date** (e.g. `20/10/2026` or immediate)
- **Title:** Senior Full-Stack AI Engineer | React, Node.js & Machine Learning Integration
- **Contact:** `+18059007207` | `m.hesam.moradian@gmail.com` | `linkedin.com/in/m-hesam-moradian` | `github.com/m-hesam-moradian`
- **Location:** Ardabil Province, Iran (Targeting Relocation to Germany / Section 81a Fast-Track & EU Blue Card)
- **Academic Qualifications:**
  - **B.Sc. in Computer Software Engineering** — Islamic Azad University (IAU)
  - **German Grade Equivalency:** `1.5 (Sehr Gut)`
  - **German Anabin Database Status:** `H+ Recognized Institution and Degree`
  - **US GPA:** `≈ 3.8 / 4.0` | **Iranian Grade:** `18.5 / 20`
- **Certifications:**
  - `CS50x: Introduction to Computer Science` — Harvard University (ID: `fe673d2f-6a44-46b6-8968-3d23f71c4c9f`)
- **Key Roles (Immutable Anchors):**
  1. `The Million Project`: Senior Full-Stack Engineer (Lead) [Next.js, React, TypeScript, CouchDB, tRPC, GraphQL, Wix]
  2. `Journal of Sustainable Energy Systems`: AI & Machine Learning Engineer [PyTorch, XGBoost, Transformers, SHAP, LIME, FastAPI]
  3. `Karlancer`: Freelance Full-Stack Developer [Next.js, Node.js, Express, MongoDB, tRPC, TanStack Query, MUI]
  4. `ArmanAndish`: Frontend Developer [React, Tailwind CSS, JavaScript, SPAs]
- **Key Open-Source Projects:**
  - `Block-MLA`: 20-Node async distributed training optimizer with per-block cosine momentum & NanoGPT 60M.
  - `talentflow-ai`: Autonomous multi-agent career & document orchestrator.
  - `techaxon-auth`: Traefik v3.7 reverse proxy, local mkcert SSL, CouchDB, Redis, and NestJS IAM microservice.
  - `theMillionProject-feeds`: Next.js 13.5 App Router + Wix Velo social feed platform.
  - `lms-platform`: Next.js, Apollo GraphQL, tRPC, CouchDB, and dark theme UI.
- **Skill Bank:** 187 verified technical skills across 23 categories.

### ⚠️ Anti-Hallucination Guardrail Rule:
The agent **never** includes skills, certifications, or companies that do not exist in `ultimate_profile.json`. Any invented skill is automatically stripped and logged in `hallucinations_stripped`.

---

## ⚡ 4. Autonomous Execution Steps for Incoming Jobs

When the user provides a jobs payload or triggers a run:

### Step 1: Load & Validate Profile
Verify that `F:\talentflow-ai\data\ultimate_profile.json` is loaded.

### Step 2: Ingest & Filter Jobs
1. Parse the incoming JSON jobs array.
2. Run each job through `evaluate_visa_and_role_eligibility(job)`.
3. Filter out all rejected jobs.
4. Sort passing jobs by `priority_boost` descending (Visa-sponsored first, Remote second).

### Step 3: Tailor & Compile Documents
For each eligible job:
1. Rank keywords from the job description against `profile.dynamic_template.skill_bank`.
2. Generate tailored headline & tailored executive summary linking Sam's background to the target company.
3. Select top 3 matching projects (e.g. `Block-MLA` for ML/HPC roles, `The Million Project` or `TechAxon` for Full-Stack/Next.js roles).
4. Compose a formal, customized **Motivation Letter** addressed to the hiring team at that company highlighting EU Blue Card / German Section 81a readiness.
5. Compile two crisp A4 PDFs using ReportLab:
   - `output/<sanitized_company>_<job_id>/Sam_Moradian_CV.pdf`
   - `output/<sanitized_company>_<job_id>/Sam_Moradian_Cover_Letter.pdf`
   - `output/<sanitized_company>_<job_id>/Sam_Moradian_Cover_Letter.txt`

### ⚠️ MANDATORY FILE NAMING PROTOCOL:
- **NEVER** include the target company's name in the CV or Cover Letter filenames.
- **CV / Resume filename:** MUST ALWAYS be strictly `Sam_Moradian_CV.pdf` (or `Sam_Moradian_Resume.pdf`).
- **Cover / Motivation Letter filename:** MUST ALWAYS be strictly `Sam_Moradian_Cover_Letter.pdf` (or `Sam_Moradian_Motivation_Letter.pdf`).
- **Staged files in Temp for upload:** MUST ALWAYS be staged as:
  - `C:\Users\Sam\AppData\Local\Temp\Sam_Moradian_CV.pdf`
  - `C:\Users\Sam\AppData\Local\Temp\Sam_Moradian_Cover_Letter.pdf`

### 📍 RESIDENTIAL ADDRESS PROTOCOL (CURRENT LOCATION IN IRAN):
- **Candidate Current City/Country:** `Ardabil, Iran`
- **Street Address:** `Shahrak Kowsar, Alley 2, Plot 644` (شهرک کوثر کوچه دوم قطعه 644)
- **Postal Code (PLZ):** `56196`
- **Location Field:** `Ardabil, Ardabil Province, Iran` (with readiness for Germany relocation under § 81a AufenthG / EU Blue Card)

### Step 4: Live Browser Automation & Human Handoff (NO HEADLESS)
1. **Active User Browser Mode:**
   - **Never operate in invisible/headless mode for live job applications.**
   - All browser operations MUST execute directly inside the user's **currently active Chrome browser** using Chrome DevTools MCP tools (`new_page`, `navigate_page`, `fill`, `click`, `take_snapshot`).
   - Every application URL opens as a **visible tab** in the user's existing Chrome window so they can watch live progress.
2. Auto-fill candidate contact information:
   - First Name: `Sam` (NOT Mohammad Hesam)
   - Last Name: `Moradian`
   - Full Name: `Sam Moradian`
   - Earliest Start Date / Notice Period: `Immediately` or today's date (`24/10/2026`)
   - Email: `m.hesam.moradian@gmail.com`
   - Phone: `+18059007207`
   - Street Address: `Shahrak Kowsar, Alley 2, Plot 644`
   - Postal Code (PLZ): `56196`
   - Location / City: `Ardabil, Iran`
   - LinkedIn: `https://www.linkedin.com/in/m-hesam-moradian`
   - GitHub: `https://github.com/m-hesam-moradian`
3. Upload `Sam_Moradian_CV.pdf` and `Sam_Moradian_Cover_Letter.pdf`.
4. Fill the cover letter textarea with the tailored motivation letter.
5. **Bot Authentication & Human Handoff:**
   - When a CAPTCHA (Turnstile, reCAPTCHA, hCaptcha), login wall, or custom required check is encountered, the agent **does not block or close the tab**.
   - The tab remains active in the user's browser, brought to the foreground, so the user can easily complete the authentication check and submit.
   - The agent records the status as `OPEN_IN_TAB_NEEDS_HUMAN` and seamlessly opens a new tab for the next job.

### Step 5: Final Run Report
Write a complete structured JSON report to `output/run_summary.json` and present a clean summary table to the user.

---

## 💻 5. CLI Execution Reference

```powershell
# Ingest and apply to a batch of jobs with live visible browser window
& "F:\talentflow-ai\.venv\Scripts\python.exe" -m src.auto_agent --jobs-file "F:\path\to\jobs.json" --strict-visa-remote --no-headless

# With auto-submit enabled (submits clean forms automatically)
& "F:\talentflow-ai\.venv\Scripts\python.exe" -m src.auto_agent --jobs-file "F:\path\to\jobs.json" --strict-visa-remote --no-headless --auto-submit

# Verification & Test Commands
& "F:\talentflow-ai\.venv\Scripts\python.exe" -m pytest "F:\talentflow-ai\tests" -v
& "F:\talentflow-ai\.venv\Scripts\python.exe" -m ruff check "F:\talentflow-ai\src" "F:\talentflow-ai\tests"
```
