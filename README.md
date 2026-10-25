# ZAI Job Applier (TalentFlow-AI)

> **Autonomous AI Career & Document Orchestrator**  
> Tailored ATS Resume & Motivation Letter Generation, Dynamic Profiling, Visa Sponsorship Gatekeeping, and Multi-Platform Browser Automation for Engineering Roles.

---

## 🚀 Key Capabilities

- **Dynamic Profiler:** Ingests live candidate metadata from GitHub APIs and blends it with verified identity anchors.
- **Visa Sponsorship Gatekeeper:** Automatically filters job descriptions for explicit visa/relocation signals and skips positions with strict citizenship barriers or native-level C2 restrictions.
- **Dynamic ATS PDF Tailoring Engine:** Generates pixel-perfect, ATS-optimized CVs and Motivation Letters using ReportLab without hallucinating unverified skills.
- **Multi-Platform ATS Automation:** Built to navigate and apply across leading ATS platforms including Personio, Greenhouse, AshbyHQ, Phenom People, and custom portals.
- **Human-in-the-Loop & MFA Handling:** Works seamlessly with visible browser sessions to allow natural CAPTCHA handling, OTP authentication, and identity confirmation.
- **Agent Operating Specification (`agent.md`):** Complete playbook detailing DOM event bypasses (React synthetic events, prototype value setters), batch form inspection patterns, and candidate ground truth standards.

---

## 📂 Project Architecture

```
zai-job-applier/
├── src/
│   ├── schemas/              # Pydantic v2 data models
│   │   └── models.py
│   ├── profiler/             # Candidate profiling & GitHub enrichment
│   │   └── profile_ingestor.py
│   ├── ingestion/            # Visa sponsorship & role eligibility filters
│   │   └── visa_filter.py
│   ├── tailor/               # ReportLab PDF compilation & LLM/keyword tailoring
│   │   └── document_tailor.py
│   ├── gateway/              # LiteLLM routing & offline fallback engines
│   │   └── llm_router.py
│   ├── browser_bot/          # Multi-tab Playwright browser automation
│   │   └── multi_tab_applier.py
│   └── auto_agent.py         # Unified CLI orchestrator
├── data/                     # Job datasets, candidate templates, dynamic profiles
├── tests/                    # End-to-end automated test suites
├── agent.md                  # Complete Agent Operational Specification & Protocol
├── pyproject.toml            # Project dependencies & tool configurations
└── README.md                 # Project documentation
```

---

## 🛠️ Quickstart

### 1. Prerequisites
- Python 3.11+
- Git

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/m-hesam-moradian/zai-job-applier.git
cd zai-job-applier

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -e .
```

### 3. Running Automated Tests
```bash
pytest tests/ -v
```

### 4. Running the CLI
```bash
# Initialize / refresh candidate dynamic profile
python -m src.auto_agent --init-profile

# Run pipeline on a job dataset
python -m src.auto_agent --jobs-file data/sample_jobs.json --headless
```

---

## 📋 Agent Operational Guidelines (`agent.md`)

For agents executing browser automation, refer to [`agent.md`](./agent.md) for:
- Identity Ground Truth standards
- Batch form inspection and single-shot execution patterns
- React Fiber / synthetic event bypass techniques
- ATS-specific selectors and workflows

---

## 📄 License

MIT License. Designed and engineered for autonomous career enablement.
