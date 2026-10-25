import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from src.schemas.models import JobPosting
from src.ingestion.visa_filter import evaluate_visa_and_role_eligibility

with open(r'F:\talentflow-ai\JD-Datasets\linkedin_selected_jobs_2026-10-24.json', 'r', encoding='utf-8') as f:
    raw_jobs = json.load(f)

ranked_jobs = []

for idx, j in enumerate(raw_jobs):
    job_id = str(j.get('jobId') or j.get('id') or '')
    company = j.get('company', '').strip()
    title = j.get('title', '').strip()
    loc = j.get('location', '').strip()
    apply_url = j.get('applyUrl') or j.get('url') or ''
    desc = j.get('description', '')
    is_ext = j.get('isExternalApply', False) or ('linkedin.com/jobs/view' not in apply_url and 'linkedin.com' not in apply_url)

    job_obj = JobPosting(
        id=job_id,
        source=company,
        title=title,
        company=company,
        location=loc,
        url=apply_url,
        description=desc,
    )

    is_eligible, reason, boost = evaluate_visa_and_role_eligibility(job_obj)

    ranked_jobs.append({
        'index': idx,
        'id': job_id,
        'company': company,
        'title': title,
        'location': loc,
        'url': apply_url,
        'is_external': is_ext,
        'eligible': is_eligible,
        'reason': reason,
        'boost': boost,
        'desc_preview': desc[:200].replace('\n', ' ')
    })

# Filter only eligible and external
eligible_ext = [j for j in ranked_jobs if j['eligible'] and j['is_external']]
eligible_ext.sort(key=lambda x: x['boost'], reverse=True)

rejected = [j for j in ranked_jobs if not j['eligible']]

print(f"Total jobs: {len(ranked_jobs)}")
print(f"Eligible External ATS Jobs: {len(eligible_ext)}")
print(f"Rejected / Blocked Jobs: {len(rejected)}\n")

print("=== TOP ELIGIBLE EXTERNAL ATS JOBS ===")
for j in eligible_ext:
    print(f"[{j['index']}] Boost: +{j['boost']} | {j['company']} | {j['title']} | Loc: {j['location']}")
    print(f"    URL: {j['url']}")
    print(f"    Reason: {j['reason']}\n")

print("\n=== REJECTED JOBS SAMPLE ===")
for j in rejected[:5]:
    print(f"[{j['index']}] {j['company']} - {j['title']}: {j['reason']}")
