import fitz
import re
import json

doc = fitz.open(r"C:\Users\HP\Downloads\bbhc league.pdf")
links = []
for page in doc:
    for link in page.get_links():
        if 'uri' in link:
            uri = link['uri']
            match = re.search(r'id=([a-zA-Z0-9_-]+)', uri)
            if not match:
                match = re.search(r'/d/([a-zA-Z0-9_-]+)', uri)
            if match:
                uri = f"https://drive.google.com/uc?id={match.group(1)}"
            links.append(uri)

with open("d:/cricket/extracted.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

records = []
current_record = None
timestamp_pattern = re.compile(r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}$")

for line in lines:
    if line in ["Timestamp", "Name", "Class", "Roll no", "Phone Number", "Category", "Right/left", "Player photo", "https://drive.google.com"]:
        continue
    
    if timestamp_pattern.match(line):
        if current_record is not None:
            records.append(current_record)
        current_record = [line]
    else:
        if current_record is not None:
            current_record.append(line)
if current_record is not None:
    records.append(current_record)

players_data = []
for idx, r in enumerate(records):
    # Depending on length
    if len(r) >= 7:
        ts, name, cls, roll, phone, category, side = r[:7]
    elif len(r) == 5:
        ts, name, cls, roll, phone = r[:5]
        category = "Batsman"
        side = "Right"
    else:
        # Fallback
        ts = r[0] if len(r) > 0 else ""
        name = r[1] if len(r) > 1 else ""
        cls = r[2] if len(r) > 2 else ""
        roll = r[3] if len(r) > 3 else ""
        phone = r[4] if len(r) > 4 else ""
        category = r[5] if len(r) > 5 and r[5] in ["All-rounder", "Batsman", "Bowler"] else "Batsman"
        side = r[6] if len(r) > 6 else "Right"
        
    role = f"{side} Hand {category}" if side != "Unknown" and category != "Unknown" else category
    photo_url = links[idx] if idx < len(links) else ""
        
    players_data.append({
        "name": name,
        "role": role,
        "class": cls,
        "registrationId": roll,
        "phone": phone,
        "photoUrl": photo_url
    })

with open("d:/cricket/players.json", "w", encoding="utf-8") as f:
    json.dump(players_data, f, indent=2)
print("players.json generated successfully")

