# AGENT OPERATIONAL SPECIFICATION & EXECUTION PROTOCOL (AGENT.MD)

> **Document Version:** 2.0.0  
> **Target Audience:** Autonomous Coding Agents, Browser Orchestration Agents, Human-in-the-Loop Pair Programmers  
> **Source Base:** TalentFlow-AI & Live ATS Browser Applier System  
> **Scope:** End-to-end autonomous job discovery, ATS tailoring, DOM manipulation, multi-platform form automation, identity consistency, and error-recovery protocols.

---

## 1. Candidate Ground Truth & Strict Identity Rules

When acting on behalf of the candidate, **never deviate** from these verified ground truths. Any inconsistency will fail corporate compliance or immigration verification.

### 1.1 Personal Identity
| Field | Standard Canonical Value | Notes |
| :--- | :--- | :--- |
| **Display Name** | **Sam Moradian** | **STRICT RULE:** Use "Sam Moradian" across all applications, cover letters, and communications. |
| **Legal / Official Name** | Mohammad Hesam Moradian | Use only when formal legal name is explicitly required by government/tax forms. |
| **First Name** | Sam (or Mohammad Hesam if legal required) | Default: Sam |
| **Last Name** | Moradian | Moradian |
| **Primary Email** | `m.hesam.moradian@gmail.com` | Primary contact & authentication inbox. |
| **Phone Number** | `+18059007207` | Primary contact phone (US format). Secondary: `+98912...` |
| **LinkedIn URL** | `https://www.linkedin.com/in/m-hesam-moradian` | Verified profile. |
| **GitHub URL** | `https://github.com/m-hesam-moradian` | Source code portfolio & open-source projects. |

### 1.2 Residential Address & Location (Iran Ground Truth)
| Field | Value | Notes |
| :--- | :--- | :--- |
| **Street Address** | `Shahrak Kowsar, Alley 2, Plot 644` | Persian: شهرک کوثر کوچه دوم قطعه 644 |
| **Postal Code (PLZ)** | `56196` | Verified postal code. |
| **City** | `Ardabil` | Ardabil Province |
| **Country** | `Iran` / `Islamic Republic of Iran` | ISO-2: `IR`, Select dropdowns: `Iran, Islamic Republic Of` |
| **Target Work Location** | Germany / EU (Open to all cities) | Berlin, Munich, Frankfurt, Stuttgart, Hamburg, Cologne, Düsseldorf, or Hybrid/Remote. |

### 1.3 Qualifications & Immigration Eligibility
| Field | Value |
| :--- | :--- |
| **Degree** | B.Sc. in Computer Engineering (Islamic Azad University) |
| **German Equivalency** | **German Grade 1.5 (Sehr Gut)** — Recognized on **Anabin H+** database. |
| **Certifications** | CS50x Introduction to Computer Science (Harvard University) |
| **Immigration Status** | Fully eligible for the **Accelerated Skilled Worker Procedure (§ 81a AufenthG)** and **EU Blue Card**. |
| **Availability / Start Date** | Immediate / `01.11.2026` (`2026-11-01`). |
| **Salary Expectation** | **€80,000 – €85,000 gross/year** (Default: `85000` / `85.000 € brutto/Jahr`). |
| **Languages** | English (C1 - Fluent/Full Professional), German (B1/B2 - Proficient/Working), Persian (Native), Turkish (Fluent). |

---

## 2. Mandatory File Naming Standards (Strict User Protocol)

> [!CAUTION]
> **CRITICAL VIOLATION WARNING:**  
> **NEVER include the company name, target employer, or recruiter name in the CV or Cover Letter filenames.**  
> Previous mistakes included naming files like `PwC_CV.pdf` or `Company_Cover_Letter.pdf`. This looks unprofessional and violates the user's explicit rule.

### Mandatory Filenames:
1. **Resume / CV:** Strictly `Sam_Moradian_CV.pdf`
2. **Cover Letter / Motivation Letter:** Strictly `Sam_Moradian_Cover_Letter.pdf`
3. **References / Certificates (if requested):** Strictly `Sam_Moradian_References.pdf`

### Staging Directory:
- Always stage active documents to `C:\Users\Sam\AppData\Local\Temp\` so the browser upload tool can access them cleanly without permission errors.
- Always save archival/proof copies into `F:\talentflow-ai\output\<Company_JobId>\`.

---

## 3. LinkedIn & Bot Detection Avoidance Rules

1. **NEVER use LinkedIn Easy Apply:**
   - LinkedIn utilizes aggressive bot detection, behavioral heuristics, and IP rate limits that can flag or restrict the user's account.
   - Applications must **only** be submitted through external company career portals (Greenhouse, Ashby, Personio, Lever, Workday, SuccessFactors, Phenom People, SmartRecruiters, Recruitee, etc.).
2. **Human-in-the-Loop Browser Execution:**
   - Always run automation directly in the user's **active, live Google Chrome window** via Chrome DevTools MCP tools (`chrome-devtools`).
   - Do **NOT** use silent headless background instances when user observation or OTP/CAPTCHA solving might be needed.
   - Allow the user to monitor actions live on screen.

---

## 4. High-Efficiency Token Optimization & Batch Form Execution

> [!IMPORTANT]
> **USER DIRECTIVE:**  
> *"please load the form and check the all inputs some is check some text some options please load the html and see the all input of that page and answer all in once to avoid token overusage ok its wrong that for each you ask or think for simple questions and make the script when you ran all in one answered"*

### The Anti-Pattern (What NEVER to do):
- Inspecting input 1 -> Thinking -> Asking/Filling input 1.
- Inspecting input 2 -> Thinking -> Asking/Filling input 2.
- This consumes massive context windows, incurs high token costs, and slows down execution.

### The Correct Protocol (One-Shot Inspection & Batch Execution):
1. **Step 1: Complete Form Introspection (Single Call):**
   Execute a single JavaScript function in the page that returns:
   - All input IDs, names, types, placeholders, required states, and current values.
   - All `<select>` options (values and text labels).
   - All radio button groups and labels.
   - All checkboxes and their enclosing labels.
   - All file inputs and their parent container labels.
   - All submit buttons and their disabled states.
2. **Step 2: Document Generation & Staging:**
   Compile the tailored `Sam_Moradian_CV.pdf` and `Sam_Moradian_Cover_Letter.pdf` matching the job description and stage them into `C:\Users\Sam\AppData\Local\Temp\`.
3. **Step 3: One-Shot Document Upload:**
   Make file inputs visible (`display: block; opacity: 1;`) if hidden, take a page snapshot to obtain DevTools UIDs, and call `upload_file`.
4. **Step 4: One-Shot Batch DOM Populator Script:**
   Execute a single JavaScript script that sets every value, dispatches both native DOM and React synthetic events, clicks required radio options, and sets checkboxes.
5. **Step 5: Zero-Error Validation & Submission:**
   Check `document.querySelectorAll(':invalid')`. If count is 0, trigger submit button click and verify confirmation screen and application ID.

---

## 5. Technical DOM & Framework Manipulation Patterns

### 5.1 React Synthetic Event Bypass (Crucial for React / Next.js / RJSF)
In modern React applications (Phenom People, Personio, Ashby, Greenhouse), directly setting `input.value = "foo"` will **fail** because React overrides the value setter and tracks internal state via fiber nodes.

```javascript
// Universal React Input Setter
const setNativeValue = (element, value) => {
  const valueSetter = Object.getOwnPropertyDescriptor(
    element instanceof HTMLInputElement ? window.HTMLInputElement.prototype :
    element instanceof HTMLTextAreaElement ? window.HTMLTextAreaElement.prototype :
    window.HTMLSelectElement.prototype,
    'value'
  )?.set;
  
  if (valueSetter) {
    valueSetter.call(element, value);
  } else {
    element.value = value;
  }
  
  // Dispatch full event sequence
  element.dispatchEvent(new Event('input', { bubbles: true }));
  element.dispatchEvent(new Event('change', { bubbles: true }));
  element.dispatchEvent(new Event('blur', { bubbles: true }));
};

// Calling React Synthetic Handlers Directly
const triggerReactChange = (element, value) => {
  const reactKey = Object.keys(element).find(k => 
    k.startsWith('__reactProps') || k.startsWith('__reactEventHandlers')
  );
  if (reactKey && element[reactKey] && typeof element[reactKey].onChange === 'function') {
    element[reactKey].onChange({
      target: { value: value, name: element.name, id: element.id },
      currentTarget: { value: value, name: element.name, id: element.id },
      persist: () => {},
      preventDefault: () => {},
      stopPropagation: () => {}
    });
  }
};
```

### 5.2 Checkbox Toggling inside Labels
In many frameworks, clicking a checkbox input that is nested inside `<label><input type="checkbox">...</label>` toggles the state twice if `.click()` is called on an already checked element or if both `.checked = true` and `.click()` are called together.
```javascript
// Safe Checkbox Setter
const setCheckboxSafe = (element, desiredState) => {
  if (!element) return;
  if (element.checked !== desiredState) {
    element.click(); // Click naturally triggers React/framework state changes
  }
};
```

### 5.3 Handling Hidden File Inputs
Many ATS platforms hide `<input type="file">` behind styled buttons or drag-and-drop divs. Chrome DevTools MCP `upload_file` requires an element UID from `take_snapshot`. If the input is hidden, the accessibility tree omits it.
```javascript
// Force File Input Visibility for DevTools Snapshotting
const unhideFileInputs = () => {
  document.querySelectorAll('input[type="file"]').forEach(el => {
    el.style.display = 'block';
    el.style.visibility = 'visible';
    el.style.opacity = '1';
    el.style.position = 'relative';
    el.style.width = '200px';
    el.style.height = '40px';
    el.removeAttribute('hidden');
    el.removeAttribute('tabindex');
  });
};
```

---

## 6. ATS Platform Playbooks & Architectural Nuances

### 6.1 Personio (`*.jobs.personio.de` / `*.jobs.personio.com`)
- **Key Characteristics:** Clean, standard HTML form. Turnstile (`cf-turnstile-response`) is often pre-rendered.
- **File Input IDs:**
  - `#doc-input-cv`: Primary CV (required).
  - `#doc-input-cover-letter`: Cover Letter (required or optional).
  - `#doc-input-other`: Certificates / Additional documents.
- **Submission Trigger:** Button with text `Send application` or class `.career-submit-application-btn`. Automatically enables when required fields and valid files are attached.
- **Success Signal:** Confirmation heading `Thanks` or `Thank you! We have received your application...`.

### 6.2 Greenhouse (`job-boards.greenhouse.io` / `boards.greenhouse.io`)
- **Key Characteristics:** Multipart form (`#application_form`).
- **File Upload:** Input `input[type="file"]#resume` and `input[type="file"]#cover_letter`.
- **Custom Questions:** Often includes boolean dropdowns ("Are you legally authorized to work in...", "Will you now or in the future require sponsorship...").
- **Success Signal:** Redirect to `/confirmation` or "Thank you for applying".

### 6.3 AshbyHQ (`jobs.ashbyhq.com`)
- **Key Characteristics:** React SPA with accessible comboboxes and rich text inputs.
- **File Upload:** Dedicated dropzone with hidden file input.
- **Phone Input:** Requires international prefix (+1 or +98).
- **Success Signal:** "Application Submitted!" dialog.

### 6.4 Phenom People / SuccessFactors (e.g. PwC Deutschland)
- **Key Characteristics:** Multi-step wizard (`step=1&stepname=username` -> `step=2&stepname=personalInformation`).
- **Two-Factor Authentication:** Sends 6-digit OTP code to applicant's email (`recruiting@jobalerts-de.pwc.com`).
- **Verification Flow:** Read Gmail inbox at `https://mail.google.com/mail/u/1/#inbox`, extract 6-digit code, paste into inputs `0-otp` through `5-otp`.
- **Form Architecture:** Built on React JSON Schema Form (`rjsf`). Handles submission via `POST /applySubmit` JSON payload returning `jobApplicationId`.
- **Success Signal:** URL redirect to `/applythankyou?status=success&jobApplicationId=...`.

### 6.5 CHECK24 Career Portal (`jobs.check24.de`)
- **Key Characteristics:** Django backend with CSRF token and custom location autocomplete.
- **Location Field:** Requires typing "Ardabil" into `#id_location_query` and clicking the dynamically rendered autocomplete pill `ul.rounded-xl button` to populate `#id_location_payload`.
- **Success Signal:** URL redirect to `/apply/success/`.

---

## 7. Professional ATS PDF Tailoring Protocol

When generating tailored CVs and Motivation Letters using ReportLab:

1. **No Hallucinations:**
   - Prioritize skills matching the JD from the candidate's verified skill bank:
     `Python, TypeScript, JavaScript, React, Next.js, FastAPI, LangGraph, LiteLLM, LangChain, PyTorch, Scikit-learn, XGBoost, PostgreSQL, Docker, GitHub Actions, CI/CD, Playwright, REST APIs, GraphQL, CouchDB, Redis`.
   - Never inject technologies the candidate does not know (e.g., COBOL, Rust, SAP ABAP).
2. **ATS Layout Principles:**
   - Standard A4 page size with 14–18mm margins.
   - Clean, single-column or clean structured layout.
   - Text rendered as real selectable vector text (never raster images).
   - Use standard Helvetica / Helvetica-Bold fonts.
   - Include distinct, professional corporate accent colors (e.g., Deep Blue, Teal, Slate).
3. **Immigration Anchor:**
   - Always include the candidate's visa qualification anchor:
     *"B.Sc. in Computer Engineering (Islamic Azad University, German Grade Equivalent 1.5 Sehr Gut, Anabin H+). Eligible for Accelerated Skilled Worker procedure (§ 81a AufenthG) and EU Blue Card."*

---

## 8. Verification, Proof, and Logging Protocol

1. **Instant Screenshot Capture:**
   Immediately upon seeing the confirmation message or URL redirect, capture a full-viewport screenshot using `take_screenshot`.
2. **File Persistence:**
   Save proof screenshot as `submitted_confirmation.png` in the job's dedicated output folder `F:\talentflow-ai\output\<Company_JobId>\`.
3. **Artifact Creation:**
   Generate a user-facing markdown artifact in the brain directory with:
   - Role Title & Job ID
   - Company Name
   - Submission Timestamp
   - Confirmation URL & Application ID (if provided)
   - Summary of details submitted
   - Embedded screenshot proof

---

## 9. Master Checklist for New Applications

- [ ] Verify role is on external career site (NOT LinkedIn Easy Apply).
- [ ] Inspect full form DOM in one single shot (gather all input IDs, types, and labels).
- [ ] Generate tailored `Sam_Moradian_CV.pdf` and `Sam_Moradian_Cover_Letter.pdf`.
- [ ] Verify filename strictness (NO employer name in filenames).
- [ ] Stage PDFs to `C:\Users\Sam\AppData\Local\Temp\`.
- [ ] Make file inputs visible and upload both documents.
- [ ] Populate all personal details via one-shot batch script using native value setters.
- [ ] Verify candidate name is **Sam Moradian**.
- [ ] Set Iranian address (Shahrak Kowsar, Alley 2, Plot 644, PLZ 56196, Ardabil, Iran).
- [ ] Set phone (`+18059007207`) and email (`m.hesam.moradian@gmail.com`).
- [ ] Answer salary expectation (€85,000) and German level (B1/B2).
- [ ] Check required privacy / data consent checkboxes safely.
- [ ] Verify zero `:invalid` fields on form.
- [ ] Submit application.
- [ ] Capture proof screenshot, record Application ID, and generate confirmation artifact.

---

## 10. Autonomous Auto-Submit & Email Magic Link Protocol (Strict User Directive)

### 10.1 Autonomous Auto-Submit (Never Add Unnecessary Human-in-the-Loop)
- When all required form fields, custom questions, and documents (`Sam_Moradian_CV.pdf`, `Sam_Moradian_Cover_Letter.pdf`) are populated and verified, the agent **MUST autonomously click the final Submit / Apply button** (`Submit Application`, `Bestätigen & bewerben`, `Send application`).
- Do NOT stop or ask the human to click submit when the form is valid and complete. Human intervention is reserved strictly for active CAPTCHA challenges or login credentials that cannot be bypassed.

### 10.2 Autonomous Email Magic Link & Verification Resolution
- When an application platform (e.g. Join.com, Otta, Workday) sends an email verification, magic sign-in link, or confirmation code, the agent has full direct access to the candidate's active Gmail inbox at:
  `https://mail.google.com/mail/u/1/#inbox`
- The agent must autonomously navigate to Gmail in an active tab, locate the newest incoming email from the ATS/employer, extract the authentication link or code, navigate to it, and complete the verification without escalating to the user.

### 10.3 Single Sign-On (Google OAuth) Protocol
- When offered the option to "Continue with Google" / "Sign in with Google", select the primary application Google account:
  **`Sam Moradian (m.hesam.moradian@gmail.com)`**
- This bypasses magic links and instantly completes authentication in a single click.
