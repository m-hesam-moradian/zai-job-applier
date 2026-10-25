from pathlib import Path

file_path = Path("F:/talentflow-ai/src/tailor/document_tailor.py")
content = file_path.read_text(encoding="utf-8")

old_code = '''    sorted_skills = _keyword_match_score(job.description, dt.skill_bank)

    clean_skills, hallucinations_stripped = _apply_anti_hallucination_guardrail(
        dt.skill_bank, sorted_skills
    )

    match_score = _compute_match_score(job.description, clean_skills)'''

new_code = '''    full_job_context = f"{job.title} {job.description}"
    sorted_skills = _keyword_match_score(full_job_context, dt.skill_bank)

    clean_skills, hallucinations_stripped = _apply_anti_hallucination_guardrail(
        dt.skill_bank, sorted_skills
    )

    match_score = _compute_match_score(full_job_context, clean_skills)'''

assert old_code in content, "old_code not found in document_tailor.py"
content = content.replace(old_code, new_code)
file_path.write_text(content, encoding="utf-8")
print("Updated full_job_context in tailor_application_for_job!")
