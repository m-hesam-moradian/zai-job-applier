import json
import sys

# Force UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

with open(r'F:\talentflow-ai\JD-Datasets\linkedin_selected_jobs_2026-10-24.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

print(f"Total jobs in 2026-10-24 dataset: {len(jobs)}\n")

external_jobs = []
easy_apply_jobs = []

for idx, j in enumerate(jobs):
    job_id = str(j.get('jobId') or j.get('id') or '')
    company = j.get('company', '').strip()
    title = j.get('title', '').strip()
    loc = j.get('location', '').strip()
    apply_url = j.get('applyUrl') or j.get('url') or ''
    is_ext = j.get('isExternalApply', False) or ('linkedin.com/jobs/view' not in apply_url and 'linkedin.com' not in apply_url)
    desc = j.get('description', '')

    job_info = {
        'index': idx,
        'job_id': job_id,
        'company': company,
        'title': title,
        'location': loc,
        'apply_url': apply_url,
        'is_external': is_ext,
        'desc_len': len(desc)
    }

    if is_ext:
        external_jobs.append(job_info)
    else:
        easy_apply_jobs.append(job_info)

print(f"=== EXTERNAL ATS JOBS ({len(external_jobs)}) ===")
for j in external_jobs:
    print(f"[{j['index']}] ID={j['job_id']} | {j['company']} | {j['title']} | Loc: {j['location']} | URL: {j['apply_url']}")

print(f"\n=== LINKEDIN EASY APPLY JOBS ({len(easy_apply_jobs)}) ===")
for j in easy_apply_jobs[:10]:
    print(f"[{j['index']}] ID={j['job_id']} | {j['company']} | {j['title']} | Loc: {j['location']}")
if len(easy_apply_jobs) > 10:
    print(f"... and {len(easy_apply_jobs) - 10} more Easy Apply jobs.")
