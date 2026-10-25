import json

with open(r'C:\Users\Sam\.gemini\antigravity\brain\1c301a54-a3ee-424d-acec-c03bf2f5e997\.system_generated\logs\transcript_full.jsonl', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i in [167, 168]:
            obj = json.loads(line)
            print(f"--- Line {i} ({obj.get('type')}) ---")
            print(obj.get('content', '')[:3000])
