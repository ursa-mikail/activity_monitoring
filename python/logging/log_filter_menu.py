from datetime import datetime
import re
import os

# Constants
LOG_FILE = "log_data.txt"  # Replace with your actual log file name
TIMESTAMP_REGEX = r"\[(\d{4}-\d{2}-\d{2}_\d{4}hr_\d{2}sec)\]"

# Function to parse logs
def parse_logs(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    entries = re.findall(rf"{TIMESTAMP_REGEX}\n+\"\"\"(.*?)\"\"\"", content, re.DOTALL)
    parsed = [
        (datetime.strptime(ts, "%Y-%m-%d_%H%Mhr_%Ssec"), msg.strip())
        for ts, msg in entries
    ]
    parsed.sort(key=lambda x: x[0])  # Ensure sorted by time
    return parsed

# Function to filter logs
def filter_logs(logs, option):
    if option == "1":  # Latest update
        return [logs[-1]]

    elif option == "2":  # By year/month or range
        start = input("Enter start date (YYYY-MM or YYYY or YYYY-MM-DD): ").strip()
        end = input("Enter end date (same format): ").strip()

        def date_filter(log):
            log_date = log[0]
            fmt = "%Y-%m-%d" if "-" in start and len(start) > 7 else ("%Y-%m" if "-" in start else "%Y")
            s = datetime.strptime(start, fmt)
            e = datetime.strptime(end, fmt)
            return s <= log_date <= e

        return list(filter(date_filter, logs))

    elif option == "3":  # By keyword(s)
        keywords = input("Enter keywords separated by space: ").strip().lower().split()
        return [
            log for log in logs
            if all(k in log[1].lower() for k in keywords)
        ]

    elif option == "4":  # By entry number
        nums = input("Enter entry numbers separated by space (e.g., 1 2 3): ").strip().split()
        indices = [int(n)-1 for n in nums if n.isdigit()]
        return [logs[i] for i in indices if 0 <= i < len(logs)]

    else:
        print("Invalid option.")
        return []

# Main menu
def main():
    if not os.path.exists(LOG_FILE):
        print(f"Log file {LOG_FILE} not found.")
        return

    logs = parse_logs(LOG_FILE)
    while True:
        print("\nLog Filter Menu")
        print("1. Get latest update")
        print("2. Filter by date (year/month/day range)")
        print("3. Filter by keyword(s)")
        print("4. Get by entry number(s)")
        print("Q. Quit")

        choice = input("Choose an option: ").strip().upper()
        if choice == "Q":
            break

        filtered = filter_logs(logs, choice)
        for i, (ts, msg) in enumerate(filtered, 1):
            print(f"\n[{ts.strftime('%Y-%m-%d_%H%Mhr_%Ssec')}]\n\"\"\"\n{msg}\n\"\"\"")

if __name__ == "__main__":
    main()


"""
A tool with menu to filter and view logs using guided options:
1. Get latest update
2. Filter by date (year/month/day range)
3. Filter by keyword(s)
4. Get by entry number(s)

refer: readme.log_filter_menu.py.md
"""