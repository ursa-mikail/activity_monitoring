Log Filter Menu
1. Get latest update
2. Filter by date (year/month/day range)
3. Filter by keyword(s)
4. Get by entry number(s)
Q. Quit
Choose an option: 2
Enter start date (YYYY-MM or YYYY or YYYY-MM-DD): 2025-05-11
Enter end date (same format): 2025-05-11

Log Filter Menu
1. Get latest update
2. Filter by date (year/month/day range)
3. Filter by keyword(s)
4. Get by entry number(s)
Q. Quit
Choose an option: 2
Enter start date (YYYY-MM or YYYY or YYYY-MM-DD): 2025-05-11
Enter end date (same format): 2025-05-12

[2025-05-11_0038hr_34sec]
"""
:
"""

Log Filter Menu
1. Get latest update
2. Filter by date (year/month/day range)
3. Filter by keyword(s)
4. Get by entry number(s)
Q. Quit
Choose an option: 3
Enter keywords separated by space: segmentation fault

[2025-05-19_1134hr_10sec]
"""
:
"""

Log Filter Menu
1. Get latest update
2. Filter by date (year/month/day range)
3. Filter by keyword(s)
4. Get by entry number(s)
Q. Quit
Choose an option: 4
Enter entry numbers separated by space (e.g., 1 2 3): 1

[2025-05-10_1140hr_36sec]
"""
:
"""

Log Filter Menu
1. Get latest update
2. Filter by date (year/month/day range)
3. Filter by keyword(s)
4. Get by entry number(s)
Q. Quit
Choose an option: q


## To create non-sensitive log for tool test:
```
# Create a sample log_data.txt file with entries in the expected format

log_entries = """
[2025-05-18_1545hr_12sec]
\"\"\"
System boot completed. All services running.
\"\"\"

[2025-05-19_1012hr_33sec]
\"\"\"
User login detected: user_id=admin
\"\"\"

[2025-05-19_1045hr_08sec]
\"\"\"
Security scan initiated on core directories.
\"\"\"

[2025-05-19_1200hr_45sec]
\"\"\"
Error: Disk usage exceeded 90% on /dev/sda1
\"\"\"

[2025-05-20_0800hr_00sec]
\"\"\"
Maintenance window started. Services temporarily offline.
\"\"\"
"""

# Save to log_data.txt
log_file_path = "/home/<user_id>/log_data.txt"  # "/mnt/data/logs.txt"
with open(log_file_path, "w") as file:
    file.write(log_entries.strip())

log_file_path
```