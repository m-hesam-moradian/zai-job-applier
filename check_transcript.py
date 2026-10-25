import json

with open(r'C:\Users\Sam\.gemini\antigravity\brain\1c301a54-a3ee-424d-acec-c03bf2f5e997\.system_generated\logs\transcript.jsonl', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 151 <= i <= 180:
            obj = json.loads(line)
            if obj.get('tool_calls'):
                for tc in obj['tool_calls']:
                    print(f"Line {i} {tc.get('name')}: {tc.get('args')}")
