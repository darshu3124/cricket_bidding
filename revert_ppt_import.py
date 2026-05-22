"""Revert BPL.pptx import: remove BPL players, restore prior photo URLs."""
import json
import re
from pathlib import Path

PLAYERS_JSON = Path(r"d:\cricket\players.json")
OUT_DIR = Path(r"d:\cricket\public\player_photos")

# Players who received PPT photos (restore Drive URLs from pre-import state)
RESTORE_PHOTOS = {
    "BCM24166": "https://drive.google.com/uc?id=1Q983M-DRdsdposfwwiWYsp5oaiFUQlLA",
    "BBA24073": "https://drive.google.com/uc?id=15FWzwM38a0x2KaxMg7w0yOe0e-_8rzkB",
    "BBA24022": "https://drive.google.com/uc?id=1mQRcrp6iDi30KILfQEYkRESKmtNteqiK",
    "BCM25201": "https://drive.google.com/uc?id=1twdHERPpp9FgXHJoXLW_M5at_Z5hCkZ5",
    "BBA24023": "https://drive.google.com/uc?id=1Y7H8z3JSbenUAiANlNGygNRy-PXCGPBq",
    "BCM23321": "https://drive.google.com/uc?id=1ziit4TmahyI_eaQw9ZNX0HpkzvzTazBD",
}


def norm_roll(reg_id):
    return re.sub(r"[^a-zA-Z0-9]", "", (reg_id or "")).upper()


def main():
    players = json.load(PLAYERS_JSON.open(encoding="utf-8"))
    removed = []
    restored = []

    kept = []
    for p in players:
        roll = norm_roll(p.get("registrationId"))
        if roll.startswith("BPL"):
            removed.append(f"{p['name']} ({p.get('registrationId')})")
            # delete ppt image file
            if p.get("photoUrl", "").startswith("/player_photos/"):
                f = OUT_DIR / p["photoUrl"].split("/")[-1]
                if f.exists():
                    f.unlink()
            continue

        if roll in RESTORE_PHOTOS and p.get("photoUrl", "").startswith("/player_photos/"):
            # remove ppt-sourced file for this roll if not a manual upload
            if roll not in ("BCA23090", "BCM23292", "BCA25001"):  # keep manual photos
                f = OUT_DIR / p["photoUrl"].split("/")[-1]
                if f.exists() and roll in RESTORE_PHOTOS:
                    try:
                        f.unlink()
                    except OSError:
                        pass
            p["photoUrl"] = RESTORE_PHOTOS[roll]
            restored.append(f"{p['name']} ({roll})")

        kept.append(p)

    json.dump(kept, PLAYERS_JSON.open("w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Players: {len(players)} -> {len(kept)}")
    if removed:
        print("Removed:")
        for r in removed:
            print(f"  - {r}")
    if restored:
        print("Restored Drive photos:")
        for r in restored:
            print(f"  * {r}")


if __name__ == "__main__":
    main()
