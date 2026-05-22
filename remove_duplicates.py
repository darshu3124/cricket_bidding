import json

with open('d:/cricket/players.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

unique_players = []
seen = set()

for p in data:
    name = p.get('name', '').strip().lower()
    reg_id = p.get('registrationId', '').strip().lower().replace(" ", "")
    phone = p.get('phone', '').strip().lower()
    
    key = (name, reg_id, phone)
    if key not in seen:
        seen.add(key)
        unique_players.append(p)
    else:
        print(f"Removed duplicate: {p.get('name')} ({p.get('registrationId')})")

with open('d:/cricket/players.json', 'w', encoding='utf-8') as f:
    json.dump(unique_players, f, indent=2)

print(f"\nOriginal count: {len(data)}")
print(f"Final count: {len(unique_players)}")
