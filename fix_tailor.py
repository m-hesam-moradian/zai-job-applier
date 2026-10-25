from pathlib import Path

file_path = Path("F:/talentflow-ai/src/tailor/document_tailor.py")
content = file_path.read_text(encoding="utf-8")

# Let's inspect the exact lines around line 43 to 75
lines = content.splitlines()

# We can replace the function directly
new_func_lines = [
    "def _score_skill_ats(skill: str, desc_lower: str) -> float:",
    '    """Score a skill against the job description using token-level & compound phrase matching."""',
    "    s_lower = skill.lower()",
    "    score = 0.0",
    "",
    "    common_stop = {",
    '        "systems", "system", "design", "development", "engineering",',
    '        "architecture", "and", "with", "for", "the", "via", "using",',
    '        "into", "from", "management", "solutions", "scalable", "high",',
    '        "level", "based", "runtime", "framework", "library", "tools",',
    "    }",
    "",
    "    # 1. Base technology name (strip parentheses, version numbers, and stop phrases)",
    '    cleaned = re.sub(r"\\(.*?\\)", "", s_lower)',
    '    cleaned = re.sub(r"\\b\\d+(\\.[\\w\\+]+)?(\\+)?\\b", "", cleaned)',
    '    cleaned = re.sub(r"\\b(runtime|framework|library)\\b", "", cleaned).strip()',
    "",
    '    parts = [p.strip() for p in re.split(r"[/,&]", cleaned) if p.strip()]',
    "    for p in parts:",
    "        if p and p in desc_lower and p not in common_stop:",
    '            if re.search(r"\\b" + re.escape(p) + r"\\b", desc_lower):',
    "                score += 50.0",
    "            else:",
    "                score += 25.0",
    "",
    "    # 2. Match acronyms and terms inside parentheses, e.g. (GCP), (LoRA), (RAG), (App Router)",
    '    for inner in re.findall(r"\\((.*?)\\)", s_lower):',
    '        for term in re.split(r"[/,&]", inner):',
    "            term = term.strip()",
    "            if term and term in desc_lower and term not in common_stop:",
    '                if re.search(r"\\b" + re.escape(term) + r"\\b", desc_lower):',
    "                    score += 40.0",
    "                else:",
    "                    score += 20.0",
    "",
    "    # 3. Token-level matches for meaningful words (>= 3 chars)",
    '    tokens = set(re.findall(r"[a-zA-Z0-9_\\-\\.+#]+", s_lower)) - common_stop',
    "    for tok in tokens:",
    "        if len(tok) >= 3:",
    '            matches = len(re.findall(r"\\b" + re.escape(tok) + r"\\b", desc_lower))',
    "            if matches > 0:",
    "                score += min(matches, 3) * 8.0",
    "",
    "    return score",
]

# Find start and end of _score_skill_ats
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if line.startswith("def _score_skill_ats("):
        start_idx = i
    if start_idx != -1 and i > start_idx and line.startswith("def _keyword_match_score("):
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    lines = lines[:start_idx] + new_func_lines + ["", ""] + lines[end_idx:]
    file_path.write_text("\n".join(lines), encoding="utf-8")
    print("Successfully replaced _score_skill_ats with proper raw strings!")
else:
    print(f"Could not locate function boundaries: start={start_idx}, end={end_idx}")
