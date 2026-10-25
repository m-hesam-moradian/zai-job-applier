import json

with open(r'C:\Users\Sam\.gemini\antigravity\brain\1c301a54-a3ee-424d-acec-c03bf2f5e997\.system_generated\logs\transcript_full.jsonl', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i == 168:
            obj = json.loads(line)
            with open('F:/talentflow-ai/original_cv_extracted.txt', 'w', encoding='utf-8') as out:
                out.write(obj.get('content', ''))
            print('Saved original_cv_extracted.txt')
            break
