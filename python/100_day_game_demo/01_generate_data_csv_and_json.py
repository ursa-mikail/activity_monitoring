#!pip install faker
import csv
from faker import Faker
import json
import random
from datetime import datetime, timedelta

# Initialize faker
fake = Faker()

# Generate 20 days of data
def generate_timeline_data():
    categories = ['pneuma', 'psyche', 'soma', 'opus', 'kismet']
    data = []
    
    # Start from today and go back 20 days
    end_date = datetime.now()
    
    for i in range(20):
        timestamp = (end_date - timedelta(days=19-i)).strftime('%Y-%m-%d')
        row = {'timestamp': timestamp}
        
        for category in categories:
            row[f'{category}.log'] = fake.sentence(nb_words=6)
            row[f'{category}.score'] = random.randint(0, 100)
        
        data.append(row)
    
    return data

# Save to CSV
def save_to_csv(data, filename='timeline_data.csv'):
    if not data:
        return
    
    fieldnames = ['timestamp'] 
    categories = ['pneuma', 'psyche', 'soma', 'opus', 'kismet']
    
    for category in categories:
        fieldnames.extend([f'{category}.log', f'{category}.score'])
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Data saved to {filename}")

# Extract to JSON for each category
def extract_to_json(csv_filename, category):
    data = []
    
    with open(csv_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            json_entry = {
                'timestamp': row['timestamp'],
                'log': row[f'{category}.log'],
                'score': int(row[f'{category}.score'])
            }
            data.append(json_entry)
    
    # Save to JSON file
    json_filename = f'{category}_data.json'
    with open(json_filename, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=2)
    
    print(f"{category.capitalize()} data extracted to {json_filename}")
    return data

# Alternative function to get JSON data without saving
def get_category_json(data, category):
    json_data = []
    
    for row in data:
        json_entry = {
            'timestamp': row['timestamp'],
            'log': row[f'{category}.log'],
            'score': int(row[f'{category}.score'])
        }
        json_data.append(json_entry)
    
    return json_data

# Generate and display the data
if __name__ == "__main__":
    # Generate timeline data
    timeline_data = generate_timeline_data()
    
    # Save to CSV
    save_to_csv(timeline_data)
    
    # Display first 3 rows as sample
    print("\nSample of generated data (first 3 rows):")
    print("timestamp\t\tpneuma.score\tpsyche.score\tsoma.score\topus.score\tkismet.score")
    for i in range(3):
        row = timeline_data[i]
        print(f"{row['timestamp']}\t{row['pneuma.score']}\t\t{row['psyche.score']}\t\t{row['soma.score']}\t\t{row['opus.score']}\t\t{row['kismet.score']}")
    
    # Extract each category to JSON
    categories = ['pneuma', 'psyche', 'soma', 'opus', 'kismet']
    
    for category in categories:
        # Extract and save to JSON files
        extract_to_json('timeline_data.csv', category)
        
        # Also demonstrate getting JSON data directly
        json_data = get_category_json(timeline_data, category)
        print(f"\n{category.capitalize()} - First entry:")
        print(json.dumps(json_data[0], indent=2))

"""
Data saved to timeline_data.csv

Sample of generated data (first 3 rows):
timestamp       pneuma.score    psyche.score    soma.score  opus.score  kismet.score
2025-09-17  67      42      68      28      53
2025-09-18  44      74      51      35      61
2025-09-19  44      2       77      66      71
Pneuma data extracted to pneuma_data.json

Pneuma - First entry:
{
  "timestamp": "2025-09-17",
  "log": "Over rise serious job father sport.",
  "score": 67
}
Psyche data extracted to psyche_data.json

Psyche - First entry:
{
  "timestamp": "2025-09-17",
  "log": "Green rather success art way easy.",
  "score": 42
}
Soma data extracted to soma_data.json

Soma - First entry:
{
  "timestamp": "2025-09-17",
  "log": "Western population serious fish.",
  "score": 68
}
Opus data extracted to opus_data.json

Opus - First entry:
{
  "timestamp": "2025-09-17",
  "log": "Morning decide account rich she style stop.",
  "score": 28
}
Kismet data extracted to kismet_data.json

Kismet - First entry:
{
  "timestamp": "2025-09-17",
  "log": "Difficult soon keep perhaps.",
  "score": 53
}
"""