with open(r'C:\Users\Sam\.gemini\antigravity\brain\1c301a54-a3ee-424d-acec-c03bf2f5e997\.system_generated\steps\646\output.txt', encoding='utf-8') as f:
    text = f.read()
for line in text.split('\n'):
    if 'Iran' in line:
        print(line)
