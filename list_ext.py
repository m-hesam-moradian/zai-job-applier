import json

with open(r'F:\talentflow-ai\JD-Datasets\linkedin_selected_jobs_2026-10-20.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

print(f"Total jobs: {len(jobs)}")
for idx, j in enumerate(jobs):
    ext = j.get('isExternalApply', False)
    url = j.get('applyUrl', '')
    if ext or 'linkedin.com' not in url:
        print(f"[{idx}] id={j.get('jobId')} | comp={j.get('company')} | title={j.get('title')} | url={url}")
