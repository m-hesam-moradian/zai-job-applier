import json

with open(r'F:\talentflow-ai\JD-Datasets\linkedin_selected_jobs_2026-10-20.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

for idx in [3, 6, 7, 18, 24]:
    j = jobs[idx]
    print(f"[{idx}] {j.get('jobId')} | {j.get('company')} | {j.get('title')} | {j.get('applyUrl')}")
