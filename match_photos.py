import json
import re
import shutil
from pathlib import Path

import fitz

PHOTO_DIR = Path(r"d:\player_photo\Player photo (File responses)")
PLAYERS_JSON = Path(r"d:\cricket\players.json")
OUT_DIR = Path(r"d:\cricket\public\player_photos")
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# Exact registrationId -> source filename (preferred over norm key)
MANUAL_MAP_EXACT = {
    "Bcm23090": "com.google.android.apps.photos.Image (1) - Prajwal Dp.pdf",
    "Bca23090": None,  # Mahesh — keep existing custom photo
    "BCM23278": "IMG_20260429_110813 - Arya S.jpg",
    "Bcm25257": "IMG_20260322_190225773 - Sathvik Acharya.jpg",
    "BCA23033": "IMG-20251129-WA0217 - Prajwal Poojary.jpg",
    "25145": "SAVE_20250830_180131 - Prajwal Shetty.jpg",
    "BCA25001": "Screenshot_20260517-214039_WhatsApp - Adhithya Adhi.png",
    "BCM23292": None,  # Harshal — keep existing custom PNG if present
}

# Normalized roll -> source (used when exact key missing)
MANUAL_MAP = {
    "BCA23078": "IMG_1600 - Darshan.jpeg",
    "BCM23211": "IMG_20250511_134740_448 - Shashank Chinnu.webp",
    "BBA23033": "20260516_143430 - Praveen Devadiga.jpg",
    "BCA23022": "IMG_0221 - Darshan Poojari.jpeg",
    "BCA24116": "IMG-20250518-WA0006 - Sharan Shetty.jpg",
    "BCM24054": "IMG-20251214-WA0174 - RODNEY DSILVA.jpg",
    "BCA23088": "IMG_20260503_172225 - Kiran kotari Kiran kotari.jpg",
    "BCM24254": "IMG_20260516_180553_570 - Maneesh Poojary.webp",
    "BCM23222": "subba - Subba Acharya.jpg",
    "BCM23360": "IMG_20250423_164140 - Winston Mendonca07.jpg",
    "BCA23110": "ASH02169 - SHARATH SHETTY.JPG",
    "BCA23034": "IMG_20260411_164944 - Prakyath Hegde.jpg",
    "BCA23035": "IMG-20260326-WA0028~2 - Prasad Bhandary.jpg",
    "BCM24166": None,
    "BBA23028": "IMG-20260405-WA0129 - Pavan Gowda.jpg",
    "BCA23096": "IMG_20260503_202037 - Nikhil Devadiga.jpg",
    "BCA23021": "1000075661 - DARSHAN GOWDA.webp",
    "BCA24086": "IMG_20250312_165611 - Deekshith Mogaveer17.jpg",
    "BCM23030": "IMG-20260513-WA0001 - Manjunath Shetty.jpg",
    "BCA23044": "Screenshot_20250513_201611 - Sampreeth Shetty.jpg",
    "BCM23170": "compressed_1000220638 - Bharath kotari.jpg",
    "BCA23070": "IMG_20250507_213838_205 - Akilesh Shetty.webp",
    "BCM25201": None,
    "BCM23162": "IMG-20260430-WA0026 - Akash Shetty.jpg",
    "BCA24045": "IMG_20260315_175545_505 - Rithik Chandan.webp",
    "BCA25063": "IMG_20260313_122857_074 - Akshay.jpg",
    "BBA24068": "IMG-20260511-WA0001 - Shrinidhi shetty.jpg",
    "BCM23166": "IMG-20260501-WA0061 - Ashish Ashish.jpg",
    "BCA25061": None,
    "BCM25239": "IMG_20251006_231630 - Prathvil.p Poojary.jpg",
    "BBA24039": "Screenshot_20260507_1642482 (1) - Nithesh Devadiga.jpg",
    "BCA25085": "94825 (1) - Rithan Martine.jpg",
    "BCM24394": "17472082611832203023352397987187 - Vikas Vikas.jpg",
    "BBA25078": "IMG-20260215-WA0009 - Rajat Poojary.jpg",
    "BBA25062": "IMG-20260126-WA0045 - Nesara Gowda.jpg",
    "25064": "IMG_20260509_144850_041 - Pavan Mogaveera.jpg",
    "BBA24006": "IMG-20250502-WA0047 - Amay N S.jpg",
    "BCA25094": "file_00000000eee071fab440c4e25b04ceb3 - Sanketh Shetty.png",
    "BCA24019": "IMG_3580 - Jeevan Jeevu.JPG",
    "BBA24023": None,
    "BCM25242": "IMG_20260224_182611_674 - Rajat Poojary.webp",
    "BCM24391": "IMG_20250510_165957_408 - Vinucshetty Shetty.webp",
    "BCM24324": "58824637549PI - Karthik k Billava.jpg",
    "BCM24332": "Screenshot_20260501_150255 - Manish Poojari.jpg",
    "BBA24022": None,
    "BCM25226": None,
    "BCA24018": "CSM_0296 - Harshith Mogaveera.jpg",
    "BCM24249": "IMG_20260427_232138_366 - Keerthiraj Poojary.webp",
    "BCM24272": "IMG_20260507_164509 - Nishanth Mogaveer.jpg",
    "BCM23145": "IMG_20250624_205347_603 - Sumanth Sumanthk.webp",
    "BCM23100": "IMG_20250509_202941_921 - Maniraj Mani.webp",
    "BBA24073": None,
    "BCM23293": "IMG_20260517_200603 - Karthik Devadiga.jpg",
    "BCA23017": "IMG_8666 - Jyothiraditya Bhat.JPG",
    "BBA23011": "IMG_20260504_185425_004 - Karthik Devadig.jpg",
    "BCA23111": "IMG_20260222_224848 - Shashi Keerthi.jpg",
    "BCA24134": "IMG_20260316_072607 - Suman Byndoor.jpg",
    "BCM24138": "IMG-20251119-WA0024 - Naveen Devadiga.jpg",
    "BCM23054": "IMG-20260516-WA0072 - Sampath Poojary.jpg",
    "BCM23321": None,
    "25036": "IMG_20260115_175301 - Sachin Mogaveer.jpg",
    "BCM24308": "IMG-20260517-WA0267 - Akash Aku.jpg",
    "BCA25169": "IMG-20260309-WA0004 - Sujan Shetty.jpg",
    "BCA25038": "IMG_20260202_133429 - Samarth kumar shetty Samarth kumar shetty.jpg",
}


def norm_id(reg_id):
    return re.sub(r"[^a-zA-Z0-9]", "", (reg_id or "")).upper()


def dest_stem(reg_id):
    """Unique filename stem — keeps Bca23090 vs Bcm23090 distinct."""
    stem = re.sub(r"[^\w]", "", reg_id or "")
    return stem or "player"


def lookup_source(reg_id):
    exact = MANUAL_MAP_EXACT.get(reg_id)
    if exact is not None:
        return exact
    return MANUAL_MAP.get(norm_id(reg_id))


def main():
    players = json.load(PLAYERS_JSON.open(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    used_sources = set()
    updated = 0
    skipped = []
    missing = []

    for player in players:
        reg = player.get("registrationId") or ""
        rid_norm = norm_id(reg)
        fname = lookup_source(reg)

        if fname is None:
            # Protected / no file — keep current local photo if any
            stem = dest_stem(reg)
            existing = OUT_DIR / f"{stem}.jpg"
            for ext in [".jpg", ".jpeg", ".png", ".webp", ".JPG", ".PNG"]:
                p = OUT_DIR / f"{stem}{ext}"
                if p.exists() and (player.get("photoUrl") or "").startswith("/player_photos/"):
                    player["photoUrl"] = f"/player_photos/{p.name}"
                    skipped.append(f"kept {player['name']} ({reg})")
                    break
            else:
                missing.append(f"{player['name']} ({reg})")
            continue

        if fname in used_sources:
            missing.append(f"{player['name']} ({reg}) — source already used: {fname}")
            continue

        src = PHOTO_DIR / fname
        if not src.exists():
            missing.append(f"{player['name']} - file not found: {fname}")
            continue

        stem = dest_stem(reg)
        if src.suffix.lower() == ".pdf":
            dest = OUT_DIR / f"{stem}.jpg"
            doc = fitz.open(src)
            doc[0].get_pixmap(dpi=150).save(dest)
            doc.close()
        else:
            dest = OUT_DIR / f"{stem}{src.suffix.lower()}"
            shutil.copy2(src, dest)

        used_sources.add(fname)
        player["photoUrl"] = f"/player_photos/{dest.name}"
        updated += 1

    json.dump(players, PLAYERS_JSON.open("w", encoding="utf-8"), indent=2, ensure_ascii=False)

    print(f"Updated {updated}/{len(players)} players")
    if skipped:
        print(f"Kept protected/custom ({len(skipped)})")
    if missing:
        print(f"No photo ({len(missing)}):")
        for m in missing:
            print(f"  - {m}")

    # Duplicate hash check
    import hashlib
    from collections import defaultdict

    by_hash = defaultdict(list)
    for p in players:
        url = p.get("photoUrl", "")
        if url.startswith("/player_photos/"):
            f = OUT_DIR / url.split("/")[-1]
            if f.exists():
                h = hashlib.md5(f.read_bytes()).hexdigest()
                by_hash[h].append((p["name"], p.get("registrationId")))
    dupes = [v for v in by_hash.values() if len(v) > 1]
    if dupes:
        print(f"\nWARNING: {len(dupes)} duplicate photo(s) still:")
        for d in dupes:
            print(" ", d)
    else:
        print("\nNo duplicate photos detected.")


if __name__ == "__main__":
    main()
