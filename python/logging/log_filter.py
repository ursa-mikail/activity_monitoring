import re
from datetime import datetime
from typing import List, Optional

LOG_PATTERN = re.compile(r"\[(\d{4}-\d{2}-\d{2}_\d{4}hr_\d{2}sec)]\n+\"\"\"(.*?)\"\"\"", re.DOTALL)

def parse_logs(text: str):
    matches = LOG_PATTERN.findall(text)
    entries = []
    for timestamp, content in matches:
        ts_clean = timestamp.replace("hr", "").replace("sec", "").replace("_", " ").replace("-", " ")
        dt = datetime.strptime(ts_clean, "%Y %m %d %H%M %S")
        entries.append({
            "datetime": dt,
            "timestamp": timestamp,
            "content": content.strip()
        })
    entries.sort(key=lambda x: x["datetime"])
    return entries

def filter_logs(
    entries,
    date_filter: Optional[str] = None,
    keyword_filter: Optional[List[str]] = None,
    entry_nums: Optional[List[int]] = None,
    latest: bool = False
):
    result = entries

    if date_filter:
        if "-" in date_filter:
            # handle range
            parts = date_filter.split("-")
            if len(parts) == 2 and len(parts[0]) == 4 and len(parts[1]) == 4:
                y_start, y_end = int(parts[0]), int(parts[1])
                result = [e for e in result if y_start <= e["datetime"].year <= y_end]
            elif len(parts[0]) == 2 and len(parts[1]) == 2:
                m_start, m_end = int(parts[0]), int(parts[1])
                result = [e for e in result if m_start <= e["datetime"].month <= m_end]
        elif len(date_filter) == 10:
            target = datetime.strptime(date_filter, "%Y-%m-%d").date()
            result = [e for e in result if e["datetime"].date() == target]
        elif len(date_filter) == 7:
            y, m = map(int, date_filter.split("-"))
            result = [e for e in result if e["datetime"].year == y and e["datetime"].month == m]
        elif len(date_filter) == 4:
            y = int(date_filter)
            result = [e for e in result if e["datetime"].year == y]

    if keyword_filter:
        keywords = [k.lower() for k in keyword_filter]
        result = [
            e for e in result
            if all(kw in e["content"].lower() for kw in keywords)
        ]

    if entry_nums:
        result = [entries[i-1] for i in entry_nums if 0 < i <= len(entries)]

    if latest:
        result = [result[-1]] if result else []

    return result

def print_entries(entries):
    for entry in entries:
        print(f"[{entry['timestamp']}]")
        print('"""')
        print(entry['content'])
        print('"""\n')

# Sample usage
if __name__ == "__main__":
    with open("log_data.txt", "r") as f:  # replace with the actual file path
        raw_text = f.read()

    all_entries = parse_logs(raw_text)

    # Guided example: filter by May to Sep
    logs = filter_logs(all_entries, date_filter="05-09")
    print("Entries from May to Sep:")
    print_entries(logs)

    # Guided example: filter by year range
    logs = filter_logs(all_entries, date_filter="1975-2025")
    print("Entries from 1975 to 2025:")
    print_entries(logs)

    # Guided example: filter by specific date
    logs = filter_logs(all_entries, date_filter="2025-05-10")
    print("Entries on 2025-05-10:")
    print_entries(logs)

    # Guided example: filter by keywords
    logs = filter_logs(all_entries, keyword_filter=["make", "nvcc"])
    print("Entries with 'make' + 'nvcc':")
    print_entries(logs)

    # Guided example: get entry 1 and 2 (by timestamp order)
    logs = filter_logs(all_entries, entry_nums=[1, 2])
    print("Entries 1 and 2:")
    print_entries(logs)

    # Guided example: get latest
    logs = filter_logs(all_entries, latest=True)
    print("Latest Entry:")
    print_entries(logs)

