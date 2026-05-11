import re
import json

with open('ccf.md', 'r', encoding='utf-8') as f:
    text = f.read()

entries = []
lines = text.split('\n')

current_type = None   # "期刊" or "会议"
current_direction = None
current_level = None  # "A", "B", "C"

for i, line in enumerate(lines):
    stripped = line.strip()

    # Match journal section header
    m = re.match(r'^#\s*中国计算机学会推荐国际学术期刊\s*$', stripped)
    if m:
        current_type = '期刊'
        # direction is on the next non-empty line in parentheses
        for j in range(i+1, min(i+5, len(lines))):
            dm = re.match(r'[（(](.+?)[）)]', lines[j].strip())
            if dm:
                current_direction = dm.group(1)
                break
        continue

    # Match conference section header
    m = re.match(r'^#\s*中国计算机学会推荐国际学术会议\s*$', stripped)
    if m:
        current_type = '会议'
        for j in range(i+1, min(i+5, len(lines))):
            dm = re.match(r'[（(](.+?)[）)]', lines[j].strip())
            if dm:
                current_direction = dm.group(1)
                break
        continue

    # Match level: 一、A类 => A, etc.
    m = re.match(r'^#\s*[一二三]、([ABC])类\s*$', stripped)
    if m:
        current_level = m.group(1)
        continue

    # Parse HTML table rows
    if '<table>' in stripped and current_type and current_direction and current_level:
        # Extract all table rows
        row_pattern = re.compile(r'<tr>(.*?)</tr>')
        rows = row_pattern.findall(stripped)
        for row in rows:
            cells = re.findall(r'<td>(.*?)</td>', row)
            if len(cells) >= 5:
                # First row is the header, skip it
                if cells[0] == '序号' or cells[0] == '':
                    continue
                seq = cells[0].strip()
                abbr = cells[1].strip() if len(cells) > 1 else ''
                fullname = cells[2].strip() if len(cells) > 2 else ''
                publisher = cells[3].strip() if len(cells) > 3 else ''
                url = cells[4].strip() if len(cells) > 4 else ''
                # Decode HTML entities
                fullname = fullname.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&#38;', '&')
                publisher = publisher.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&#38;', '&')
                entry = {
                    'type': current_type,
                    'direction': current_direction,
                    'level': current_level,
                    'seq': seq,
                    'abbr': abbr,
                    'name': fullname,
                    'publisher': publisher,
                    'url': url
                }
                entries.append(entry)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

print(f"Parsed {len(entries)} entries")
# Print unique directions, publishers, types, levels
print("Types:", set(e['type'] for e in entries))
print("Directions:", sorted(set(e['direction'] for e in entries)))
print("Levels:", sorted(set(e['level'] for e in entries)))
publishers = sorted(set(e['publisher'] for e in entries))
print("Publishers count:", len(publishers))
