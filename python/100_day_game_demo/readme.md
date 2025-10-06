# 100_day_game_demo

View interactive graphs: [option 57](https://ursa-mikail.github.io/site_announcement/)

1. Generate Sample Data
```bash
python 01_generate_data_csv_and_json.py
Creates timeline_data.csv with 20 days of fake data

Generates 5 categories: pneuma, psyche, soma, opus, kismet

Each entry has timestamp, log text, and score (0-100)
```

2. Convert Between Formats
```bash
python 02_csv_to_folder_json_to_csv.py
Converts CSV to individual JSON files

Converts JSON back to CSV

Creates organized folder structure
```

3. Visualize Data
```bash
python 03_csv_to_df_and_plot.py
Creates interactive plots using mpld3

Hover over points to see log details

Exports HTML files for web viewing
```

### Data Structure
CSV Format:
```text
timestamp,pneuma.log,pneuma.score,psyche.log,psyche.score,...
2024-01-01,"Random log text",85,"Another log",72,...
```

JSON Format (per category):

```json
[
  {
    "timestamp": "2024-01-01",
    "log": "Random log text", 
    "score": 85
  }
]
```

### Output Files
After running all scripts:
```
timeline_data.csv - Original generated data

category_json/ - Individual JSON files per category

*.html - Interactive plots for each category

combined_timeline.html - All categories in one plot
```