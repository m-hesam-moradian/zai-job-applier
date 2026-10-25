import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

json_path = Path(r"c:\Users\Sam\Downloads\linkedin_selected_jobs_2026-10-24.json")
with open(json_path, "r", encoding="utf-8") as f:
    jobs = json.load(f)

for idx in [1, 3, 5, 11, 24, 25, 27, 28, 29, 30]:
    if idx < len(jobs):
        j = jobs[idx]
        print(f"--- Job {idx+1}: {j.get('company')} | {j.get('title')} ---")
        for k, v in j.items():
            if k == "description":
                print(f"  {k}: {str(v)[:150]}...")
            else:
                print(f"  {k}: {v}")
