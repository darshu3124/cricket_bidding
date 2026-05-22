import json

with open('d:/cricket/players.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find and remove the first occurrence of Darshan
for i, p in enumerate(data):
    if p.get('name', '').lower() == 'darshan':
        print(f"Removed first Darshan: {p}")
        del data[i]
        break

with open('d:/cricket/players.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
