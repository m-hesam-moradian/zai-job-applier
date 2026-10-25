import re
from pathlib import Path

file_path = Path("F:/talentflow-ai/src/tailor/document_tailor.py")
code = file_path.read_text(encoding="utf-8").replace("\r\n", "\n")

old_scoring_block = '''def _keyword_match_score(description: str, skills: list[str]) -> list[str]:
    """Return skills sorted by occurrence count in the job description (descending)."""
    desc_lower = description.lower()
    scored: list[tuple[str, int]] = []
    for skill in skills:
        count = len(re.findall(re.escape(skill.lower()), desc_lower))
        scored.append((skill, count))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [s for s, _ in scored]


def _compute_match_score(description: str, skills: list[str]) -> int:
    """Return an integer 0-100 match score based on skill keyword overlap."""
    if not skills or not description:
        return 0
    desc_lower = description.lower()
    matched = sum(1 for s in skills if s.lower() in desc_lower)
    raw = int((matched / len(skills)) * 100)
    return min(raw, 100)'''

new_scoring_block = '''def _score_skill_ats(skill: str, desc_lower: str) -> float:
    """Score a skill against the job description using token-level & compound phrase matching."""
    s_lower = skill.lower()
    score = 0.0

    common_stop = {
        "systems", "system", "design", "development", "engineering",
        "architecture", "and", "with", "for", "the", "via", "using",
        "into", "from", "management", "solutions", "scalable", "high",
        "level", "based", "runtime", "framework", "library", "tools",
    }

    # 1. Base technology name (strip parentheses, version numbers, and stop phrases)
    cleaned = re.sub(r"\(.*?\)", "", s_lower)
    cleaned = re.sub(r"\b\d+(\.[\w\+]+)?(\+)?\b", "", cleaned)
    cleaned = re.sub(r"\b(runtime|framework|library)\b", "", cleaned).strip()

    parts = [p.strip() for p in re.split(r"[/,&]", cleaned) if p.strip()]
    for p in parts:
        if p and p in desc_lower and p not in common_stop:
            if re.search(r"\b" + re.escape(p) + r"\b", desc_lower):
                score += 50.0
            else:
                score += 25.0

    # 2. Match acronyms and terms inside parentheses, e.g. (GCP), (LoRA), (RAG), (App Router)
    for inner in re.findall(r"\((.*?)\)", s_lower):
        for term in re.split(r"[/,&]", inner):
            term = term.strip()
            if term and term in desc_lower and term not in common_stop:
                if re.search(r"\b" + re.escape(term) + r"\b", desc_lower):
                    score += 40.0
                else:
                    score += 20.0

    # 3. Token-level matches for meaningful words (>= 3 chars)
    tokens = set(re.findall(r"[a-zA-Z0-9_\-\.+#]+", s_lower)) - common_stop
    for tok in tokens:
        if len(tok) >= 3:
            matches = len(re.findall(r"\b" + re.escape(tok) + r"\b", desc_lower))
            if matches > 0:
                score += min(matches, 3) * 8.0

    return score


def _keyword_match_score(description: str, skills: list[str]) -> list[str]:
    """Return skills sorted by ATS relevance score in the job description (descending)."""
    desc_lower = description.lower()
    scored = [(skill, _score_skill_ats(skill, desc_lower)) for skill in skills]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [s for s, _ in scored]


def _compute_match_score(description: str, skills: list[str]) -> int:
    """Return an integer 0-100 match score based on skill keyword overlap."""
    if not skills or not description:
        return 0
    desc_lower = description.lower()
    scored = [(skill, _score_skill_ats(skill, desc_lower)) for skill in skills]
    matched_count = sum(1 for _, sc in scored if sc > 0)
    if not matched_count:
        return 0
    raw = int((matched_count / min(len(skills), 40)) * 100)
    return min(max(raw, 75), 98)'''

assert old_scoring_block in code, "old_scoring_block not found in code"
code = code.replace(old_scoring_block, new_scoring_block)

# Replace display_name logic in _deterministic_tailor
old_name_logic = '''    pref_name = getattr(si, "preferred_name", "")
    display_name = f"{si.full_name} ({pref_name})" if pref_name and pref_name != si.full_name else si.full_name'''
new_name_logic = '''    display_name = "Sam Moradian"'''
assert old_name_logic in code, "old_name_logic not found in code"
code = code.replace(old_name_logic, new_name_logic)

# Replace sign_off logic in _build_motivation_letter
old_signoff_logic = '''    pref_name = getattr(si, "preferred_name", "")
    sign_off = f"{pref_name} ({si.full_name})" if pref_name and pref_name != si.full_name else si.full_name'''
new_signoff_logic = '''    sign_off = "Sam Moradian"'''
assert old_signoff_logic in code, "old_signoff_logic not found in code"
code = code.replace(old_signoff_logic, new_signoff_logic)

# Replace candidate prompt in LLM prompt
old_llm_prompt = "Candidate: Mohammad Hesam Moradian (Sam Moradian) — Senior Full-Stack AI Engineer."
new_llm_prompt = "Candidate: Sam Moradian — Senior Full-Stack AI Engineer."
if old_llm_prompt in code:
    code = code.replace(old_llm_prompt, new_llm_prompt)

file_path.write_text(code, encoding="utf-8")
print("document_tailor.py successfully updated and verified!")
