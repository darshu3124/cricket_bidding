import json
import re

PLAYERS_JSON = "d:/cricket/players.json"


def norm_phone(phone):
    digits = re.sub(r"\D", "", phone or "")
    return digits[-10:] if len(digits) >= 10 else digits


with open(PLAYERS_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

unique_players = []
seen_phones = {}

for p in data:
    phone = norm_phone(p.get("phone"))

    if not phone:
        unique_players.append(p)
        continue

    if phone not in seen_phones:
        seen_phones[phone] = p
        unique_players.append(p)
        continue

    existing = seen_phones[phone]
    new_has_photo = "/player_photos/" in (p.get("photoUrl") or "")
    old_has_photo = "/player_photos/" in (existing.get("photoUrl") or "")

    if new_has_photo and not old_has_photo:
        idx = unique_players.index(existing)
        unique_players[idx] = p
        seen_phones[phone] = p
        print(f"Replaced duplicate phone {phone}: kept {p.get('name')} (was {existing.get('name')})")
    else:
        print(f"Removed duplicate phone {phone}: {p.get('name')} (kept {existing.get('name')})")

with open(PLAYERS_JSON, "w", encoding="utf-8") as f:
    json.dump(unique_players, f, indent=2, ensure_ascii=False)

print(f"\nOriginal count: {len(data)}")
print(f"Final count: {len(unique_players)}")
