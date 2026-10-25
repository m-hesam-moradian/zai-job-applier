from pathlib import Path

file_path = Path("F:/talentflow-ai/src/tailor/document_tailor.py")
content = file_path.read_text(encoding="utf-8").replace("\r\n", "\n")

old_code = '''    top_skills = selected_skills[:3] if len(selected_skills) >= 3 else selected_skills
    skills_str = " · ".join(top_skills) if top_skills else "Python · TypeScript · AI"

    tailored_headline = f"{job.title} | {skills_str}"'''

new_code = '''    clean_top: list[str] = []
    for s in selected_skills[:10]:
        base = re.sub(r"\\(.*?\\)", "", s).strip()
        base = re.sub(r"\\b\\d+(\\.[\\w\\+]+)?(\\+)?\\b", "", base).strip()
        base = re.sub(r"\\b(Runtime|Framework|Outputs|Storage|Pipelines|Inference)\\b", "", base, flags=re.IGNORECASE).strip()
        if base and base not in clean_top and len(base) <= 22:
            clean_top.append(base)
    top_headline = clean_top[:4] if len(clean_top) >= 4 else clean_top
    skills_str = " · ".join(top_headline) if top_headline else "Next.js · TypeScript · Python · AI Agents"

    tailored_headline = f"{job.title} | {skills_str}"'''

assert old_code in content, "old_code not found in document_tailor.py"
content = content.replace(old_code, new_code)
file_path.write_text(content, encoding="utf-8")
print("Clean headline logic updated in document_tailor.py!")
