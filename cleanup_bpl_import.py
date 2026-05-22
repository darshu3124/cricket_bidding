import json
import re
import shutil
from pathlib import Path

PLAYERS_JSON = Path(r"d:\cricket\players.json")
OUT_DIR = Path(r"d:\cricket\public\player_photos")

NAME_ALIASES = {
    "prathval": "prathvil",
    "kishan": "kiran kotari",
    "sampreeth": "sampreeth shetty",
    "keerthesh": "keerthiraj",
    "goutham": "goutham shetty",
    "aditya": "aditya bhat",
    "pavan": "pavan",
    "samarth": "samarth",
    "maneesh": "maneesh",
}


def norm_name(name):
    n = re.sub(r"^t+", "", (name or "").strip(), flags=re.I)
    n = re.sub(r"[^a-z0-9\s]", " ", n.lower())
    n = re.sub(r"\s+", " ", n).strip()
    return NAME_ALIASES.get(n, n)


def norm_roll(reg_id):
    return re.sub(r"[^a-zA-Z0-9]", "", (reg_id or "")).upper()


def has_local_photo(player):
    return (player.get("photoUrl") or "").startswith("/player_photos/")


def names_match(a, b):
    na, nb = norm_name(a), norm_name(b)
    if na == nb or na in nb or nb in na:
        return True
    ta, tb = set(na.split()), set(nb.split())
    return len(ta & tb) >= 1 and len(ta & tb) >= min(len(ta), len(tb)) - 1


def main():
    players = json.load(PLAYERS_JSON.open(encoding="utf-8"))
    removed = []
    merged_photos = []

    bpl_players = [
        p for p in players if str(p.get("registrationId", "")).startswith("BPL")
    ]
    core_players = [
        p for p in players if not str(p.get("registrationId", "")).startswith("BPL")
    ]

    for bpl in bpl_players:
        match_idx = None
        for i, p in enumerate(core_players):
            if names_match(bpl["name"], p["name"]):
                match_idx = i
                break

        if match_idx is None:
            continue

        existing = core_players[match_idx]
        if not has_local_photo(existing) and has_local_photo(bpl):
            bpl_src = OUT_DIR / bpl["photoUrl"].split("/")[-1]
            if bpl_src.exists():
                ext = bpl_src.suffix
                rid = norm_roll(existing.get("registrationId")) or f"player{match_idx}"
                dest = OUT_DIR / f"{rid}{ext}"
                shutil.copy2(bpl_src, dest)
                existing["photoUrl"] = f"/player_photos/{dest.name}"
                merged_photos.append(f"{existing['name']} <- {bpl['name']}")

        removed.append(f"{bpl['name']} ({bpl.get('registrationId')})")

    # Keep BPL entries that did not match anyone
    for bpl in bpl_players:
        if any(names_match(bpl["name"], p["name"]) for p in core_players):
            continue
        core_players.append(bpl)

    players = core_players

    # Dedupe by roll number
    seen = {}
    unique = []
    for p in players:
        roll = norm_roll(p.get("registrationId"))
        if roll and roll in seen:
            removed.append(f"dup roll {roll}: {p['name']}")
            continue
        if roll:
            seen[roll] = True
        unique.append(p)

    json.dump(unique, PLAYERS_JSON.open("w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Final count: {len(unique)}")
    if removed:
        print("Removed BPL duplicates:")
        for r in removed:
            print(f"  - {r}")
    if merged_photos:
        print("Merged photos:")
        for m in merged_photos:
            print(f"  * {m}")


if __name__ == "__main__":
    main()
