from pathlib import Path

file_path = Path("F:/talentflow-ai/src/tailor/document_tailor.py")
content = file_path.read_text(encoding="utf-8").replace("\r\n", "\n")

old_code = '''    clean_top: list[str] = []
    for s in selected_skills[:10]:
        base = re.sub(r"\\(.*?\\)", "", s).strip()
        base = re.sub(r"\\b\\d+(\\.[\\w\\+]+)?(\\+)?\\b", "", base).strip()
        base = re.sub(r"\\b(Runtime|Framework|Outputs|Storage|Pipelines|Inference)\\b", "", base, flags=re.IGNORECASE).strip()
        if base and base not in clean_top and len(base) <= 22:
            clean_top.append(base)
    top_headline = clean_top[:4] if len(clean_top) >= 4 else clean_top
    skills_str = " · ".join(top_headline) if top_headline else "Next.js · TypeScript · Python · AI Agents"'''

new_code = '''    def _clean_skill_label(s: str) -> str:
        if "AI Agents" in s:
            return "AI Agents"
        if "Prompt Engineering" in s:
            return "Prompt Engineering"
        if "Google Cloud Platform" in s or "(GCP)" in s:
            return "GCP"
        if "RAG" in s:
            return "RAG"
        base = re.sub(r"\\(.*?\\)", "", s).strip()
        base = re.sub(r"\\d+(\\.\\d+)?\\s*/\\s*\\d+(\\.\\d+)?\\+?", "", base)
        base = re.sub(r"\\b\\d+(\\.[a-zA-Z0-9_\\+]+)?\\+?\\b", "", base)
        base = re.sub(r"[/+]", "", base)
        base = re.sub(r"\\b(Runtime|Framework|Outputs|Storage|Pipelines|Inference|Systems?)\\b", "", base, flags=re.IGNORECASE)
        base = re.sub(r"\\s+", " ", base).strip()
        return base

    clean_top: list[str] = []
    for s in selected_skills[:12]:
        lbl = _clean_skill_label(s)
        if lbl and lbl not in clean_top and len(lbl) <= 20:
            clean_top.append(lbl)
    top_headline = clean_top[:5] if len(clean_top) >= 5 else clean_top
    skills_str = " · ".join(top_headline) if top_headline else "Next.js · TypeScript · Python · AI Agents"'''

assert old_code in content, "old_code not found in document_tailor.py"
content = content.replace(old_code, new_code)
file_path.write_text(content, encoding="utf-8")
print("Clean skill label logic updated!")
