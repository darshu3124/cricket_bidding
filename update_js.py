import re
import json

with open("d:/cricket/extracted.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

records = []
current_record = None
timestamp_pattern = re.compile(r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}$")

for line in lines:
    if line in ["Timestamp", "Name", "Class", "Roll no", "Phone Number", "Category", "Right/left", "Player photo"]:
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
for r in records:
    if len(r) == 8:
        ts, name, cls, roll, phone, category, side, photo = r
    elif len(r) == 6:
        ts, name, cls, roll, phone, photo = r
        category = "Batsman"  # default
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
        photo = r[-1] if len(r) > 0 else ""
        
    imageType = "batsman"
    if category.lower() == "bowler":
        imageType = "bowler"
    elif category.lower() == "all-rounder":
        imageType = "all_rounder"
        
    role = f"{side} Hand {category}" if side != "Unknown" and category != "Unknown" else category
        
    players_data.append({
        "name": name,
        "role": role,
        "age": "N/A",  # Not in PDF
        "team": cls,
        "registrationId": roll,
        "battingStyle": f"{side}-hand bat",
        "bowlingStyle": f"{side}-arm",
        "imageType": imageType
    })

json_str = json.dumps(players_data, indent=2)

with open("d:/cricket/src/main.js", "r", encoding="utf-8") as f:
    js_content = f.read()

# Replace the mock array
start_marker = "const playersData = ["
end_marker = "];\n\n// Mapping roles to images"

start_idx = js_content.find(start_marker)
end_idx = js_content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_js_content = js_content[:start_idx] + "const playersData = " + json_str + ";\n\n// Mapping roles to images" + js_content[end_idx + len(end_marker):]
    with open("d:/cricket/src/main.js", "w", encoding="utf-8") as f:
        f.write(new_js_content)
    print("JS updated successfully")
else:
    print("Could not find markers in JS file")
