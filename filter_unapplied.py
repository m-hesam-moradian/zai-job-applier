import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\Sam\Downloads\linkedin_selected_jobs_2026-10-24.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

submitted_ids = {
    "4476691047", "4398256080", "4461009898", "4475798351", "4477275441",
    "4427346769", "4475414167", "4481547673", "4398263346", "4479336458",
    "4482857863", "4481556177", "4472860977"
}

print(f"{'#':<3} | {'Job ID':<11} | {'Company':<25} | {'Title':<45} | {'Apply URL'}")
print("-" * 120)
count = 0
for i, j in enumerate(jobs):
    jid = str(j.get("jobId") or j.get("id"))
    if jid in submitted_ids:
        continue
    comp = j.get("company", "")[:24]
    title = j.get("title", "")[:44]
    url = j.get("applyUrl") or j.get("url") or ""
    print(f"{i+1:<3} | {jid:<11} | {comp:<25} | {title:<45} | {url[:50]}")
    count += 1

print(f"\nRemaining unapplied jobs: {count}")
