import json

with open("F:/talentflow-ai/JD-Datasets/linkedin_selected_jobs_2026-10-20.json", encoding="utf-8") as f:
    jobs = json.load(f)

for j in jobs:
    jid = str(j.get("jobId") or j.get("id"))
    if jid in ["4477275441", "4477572741", "4470109327"]:
        print("ID:", jid)
        print("Title:", repr(j.get("title")))
        print("Company:", repr(j.get("company")))
        print("URL:", repr(j.get("applyUrl") or j.get("url")))
        print("-" * 40)
