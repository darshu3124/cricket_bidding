"""
Import players from BPL.pptx: add missing entries, assign photos from slides
to players who lack a local /player_photos/ image.
"""
import json
import re
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

PPT = Path(
    r"c:\Users\HP\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\LocalState\sessions\83FD23E5B3732A6F59229BBAF620A70C8CFA94CB\transfers\2026-21\BPL.pptx"
)
PLAYERS_JSON = Path(r"d:\cricket\players.json")
OUT_DIR = Path(r"d:\cricket\public\player_photos")
OUT_DIR.mkdir(parents=True, exist_ok=True)

NAME_ALIASES = {
    "darshan gowda": "darshan gowda",
    "dp prajwal": "dp prajwal",
    "sharath shetty": "sharath",
    "shrinidhi shetty": "shrinidhi shetty",
    "sharan": "sharan shetty",
    "shashi": "shashikeerthi",
    "satvik": "sathvik",
    "prathval": "prathvil",
    "prathvil": "prathvil",
    "jeevan": "jeevanhs",
    "aditya": "aditya bhat",
    "maniraj": "mani",
    "kishan": "kiran kotari",
    "rohith shetty": "rohit shetty",
    "rajath poojary": "rajath shetty",
    "subba": "subrahmanya b",
    "keerthesh": "keerthiraj",
    "prashanth": "prashanth",
    "sunil": "sunil",
    "avinash": "avinash",
    "vinay": "vinay",
    "tmanjunath": "manjunath",
}


def norm_name(name):
    n = re.sub(r"^t+", "", (name or "").strip(), flags=re.I)
    n = re.sub(r"[^a-z0-9\s]", " ", n.lower())
    n = re.sub(r"\s+", " ", n).strip()
    return NAME_ALIASES.get(n, n)


def norm_roll(reg_id):
    return re.sub(r"[^a-zA-Z0-9]", "", (reg_id or "")).upper()


def parse_category_hand(lines):
    category = "Batsman"
    hand = "Right"
    for line in lines[1:]:
        low = line.lower().strip()
        if low in ("left", "right"):
            hand = line.strip().capitalize()
        elif "bowl" in low:
            category = "Bowler"
        elif "all" in low:
            category = "All-rounder"
        elif "bat" in low:
            category = "Batsman"
    return hand, category


def has_local_photo(player):
    url = player.get("photoUrl") or ""
    return url.startswith("/player_photos/")


def names_match(ppt_name, player_name):
    a = norm_name(ppt_name)
    b = norm_name(player_name)
    if a == b:
        return True
    if a in b or b in a:
        return True
    at = set(a.split())
    bt = set(b.split())
    return len(at & bt) >= 1 and (at <= bt or bt <= at or len(at & bt) >= max(1, min(len(at), len(bt)) - 1))


def find_player(players, ppt_name, used_indices):
    for i, p in enumerate(players):
        if i in used_indices:
            continue
        if names_match(ppt_name, p["name"]):
            return i, p
    return None, None


def extract_slide_data(slide):
    texts = []
    for shape in slide.shapes:
        if hasattr(shape, "text") and shape.text.strip():
            texts.append(shape.text.strip())

    if not texts:
        return None

    name_line = texts[0]
    hand, category = parse_category_hand(texts)
    role = f"{hand} Hand {category}"

    pictures = [s for s in slide.shapes if s.shape_type == MSO_SHAPE_TYPE.PICTURE]
    image_shape = None
    if pictures:
        image_shape = max(pictures, key=lambda s: s.width * s.height)

    return {
        "name": re.sub(r"^t+", "", name_line, flags=re.I).strip(),
        "role": role,
        "hand": hand,
        "category": category,
        "image_shape": image_shape,
    }


def save_image(shape, dest: Path):
    blob = shape.image.blob
    ext = shape.image.ext or "png"
    if not ext.startswith("."):
        ext = "." + ext
    dest = dest.with_suffix(ext)
    dest.write_bytes(blob)
    return dest


def main():
    prs = Presentation(str(PPT))
    players = json.load(PLAYERS_JSON.open(encoding="utf-8"))
    seen_rolls = {norm_roll(p.get("registrationId")) for p in players if norm_roll(p.get("registrationId"))}
    seen_phones = set()

    for p in players:
        phone = re.sub(r"\D", "", p.get("phone") or "")
        if phone:
            seen_phones.add(phone)

    ppt_players = []
    for slide_idx in range(1, len(prs.slides)):
        slide = prs.slides[slide_idx]
        data = extract_slide_data(slide)
        if data and data["name"]:
            ppt_players.append(data)

    added = []
    photos_updated = []
    used_indices = set()

    for ppt in ppt_players:
        idx, player = find_player(players, ppt["name"], used_indices)

        if player is None:
            # New player from PPT
            slug = re.sub(r"[^a-z0-9]", "", norm_name(ppt["name"]))[:20] or "player"
            reg = f"BPL_{slug.upper()}"
            n = 1
            while reg in seen_rolls:
                reg = f"BPL_{slug.upper()}_{n}"
                n += 1
            seen_rolls.add(reg)

            player = {
                "name": ppt["name"].title() if ppt["name"].islower() else ppt["name"],
                "role": ppt["role"],
                "class": "BPL",
                "registrationId": reg,
                "phone": "",
                "photoUrl": "",
            }
            players.append(player)
            idx = len(players) - 1
            added.append(player["name"])
        else:
            used_indices.add(idx)

        rid = norm_roll(player.get("registrationId")) or f"BPL_{idx}"
        dest_base = OUT_DIR / rid

        need_photo = not has_local_photo(player)
        if ppt["image_shape"] is not None and need_photo:
            saved = save_image(ppt["image_shape"], dest_base)
            player["photoUrl"] = f"/player_photos/{saved.name}"
            photos_updated.append(f"{player['name']} ({player.get('registrationId')})")

    # Second pass: assign PPT photos to any still without local photo if name matches unused ppt entry
    for ppt in ppt_players:
        if ppt["image_shape"] is None:
            continue
        for i, player in enumerate(players):
            if has_local_photo(player):
                continue
            if names_match(ppt["name"], player["name"]):
                rid = norm_roll(player.get("registrationId")) or f"BPL_{i}"
                saved = save_image(ppt["image_shape"], OUT_DIR / rid)
                player["photoUrl"] = f"/player_photos/{saved.name}"
                label = f"{player['name']} ({player.get('registrationId')})"
                if label not in photos_updated:
                    photos_updated.append(label)
                break

    json.dump(players, PLAYERS_JSON.open("w", encoding="utf-8"), indent=2, ensure_ascii=False)

    print(f"PPT players parsed: {len(ppt_players)}")
    print(f"Total in database: {len(players)}")
    if added:
        print(f"\nAdded {len(added)} new players:")
        for n in added:
            print(f"  + {n}")
    if photos_updated:
        print(f"\nPhotos added from PPT ({len(photos_updated)}):")
        for n in photos_updated:
            print(f"  * {n}")

    still_no_photo = [p["name"] for p in players if not has_local_photo(p)]
    if still_no_photo:
        print(f"\nStill no local photo ({len(still_no_photo)}):")
        for n in still_no_photo:
            print(f"  - {n}")


if __name__ == "__main__":
    main()
