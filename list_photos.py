import json
import re
from pathlib import Path

PHOTO_DIR = Path(r"d:\player_photo\Player photo (File responses)")
players = json.load(open(r"d:\cricket/players.json", encoding="utf-8"))


def extract(fn):
    s = Path(fn).stem
    if " - " in s:
        s = s.rsplit(" - ", 1)[1]
    return re.sub(r"\(\d+\)$", "", s).strip()


files = sorted(
    [
        (extract(f.name), f.name)
        for f in PHOTO_DIR.iterdir()
        if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp", ".gif"]
    ],
    key=lambda x: x[0].lower(),
)
for label, fn in files:
    print(f"{label:40} | {fn}")
print("---PLAYERS---")
for p in players:
    print(f"{p.get('registrationId',''):12} {p['name']}")
