import pandas as pd
import json
import os
import glob
from pathlib import Path

def csv_to_json(csv_folder='.', output_folder=None, csv_filename=None):
    """
    Convert CSV files to JSON format
    
    Args:
        csv_folder (str): Folder containing CSV files (default: current directory)
        output_folder (str): Folder to save JSON files (default: same as csv_folder)
        csv_filename (str): Specific CSV file to convert (default: all CSV files in folder)
    
    Returns:
        list: Paths to created JSON files
    """
    if output_folder is None:
        output_folder = csv_folder
    
    # Create output folder if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    json_files = []
    
    # Handle single file or all CSV files
    if csv_filename:
        csv_files = [os.path.join(csv_folder, csv_filename)]
    else:
        csv_files = glob.glob(os.path.join(csv_folder, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {csv_folder}")
        return []
    
    for csv_file in csv_files:
        try:
            # Read CSV file
            df = pd.read_csv(csv_file)
            
            # Create base filename
            base_name = os.path.splitext(os.path.basename(csv_file))[0]
            json_file = os.path.join(output_folder, f"{base_name}.json")
            
            # Convert to JSON
            json_data = df.to_dict(orient='records')
            
            # Save JSON file
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            json_files.append(json_file)
            print(f"✓ Converted {csv_file} -> {json_file} ({len(json_data)} records)")
            
        except Exception as e:
            print(f"✗ Error converting {csv_file}: {e}")
    
    return json_files

def json_to_csv(json_folder='.', output_folder=None, json_filename=None):
    """
    Convert JSON files to CSV format
    
    Args:
        json_folder (str): Folder containing JSON files (default: current directory)
        output_folder (str): Folder to save CSV files (default: same as json_folder)
        json_filename (str): Specific JSON file to convert (default: all JSON files in folder)
    
    Returns:
        list: Paths to created CSV files
    """
    if output_folder is None:
        output_folder = json_folder
    
    # Create output folder if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    csv_files = []
    
    # Handle single file or all JSON files
    if json_filename:
        json_files = [os.path.join(json_folder, json_filename)]
    else:
        json_files = glob.glob(os.path.join(json_folder, "*.json"))
    
    if not json_files:
        print(f"No JSON files found in {json_folder}")
        return []
    
    for json_file in json_files:
        try:
            # Read JSON file
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # Convert to DataFrame
            df = pd.DataFrame(json_data)
            
            # Create base filename
            base_name = os.path.splitext(os.path.basename(json_file))[0]
            csv_file = os.path.join(output_folder, f"{base_name}.csv")
            
            # Save CSV file
            df.to_csv(csv_file, index=False)
            
            csv_files.append(csv_file)
            print(f"✓ Converted {json_file} -> {csv_file} ({len(df)} records)")
            
        except Exception as e:
            print(f"✗ Error converting {json_file}: {e}")
    
    return csv_files

def csv_to_json_by_category(csv_file='timeline_data.csv', output_folder='json_data'):
    """
    Convert the timeline CSV to individual JSON files for each category
    
    Args:
        csv_file (str): Path to the timeline CSV file
        output_folder (str): Folder to save category JSON files
    
    Returns:
        dict: Mapping of category to JSON file paths
    """
    try:
        # Read CSV file
        df = pd.read_csv(csv_file)
        
        # Create output folder
        Path(output_folder).mkdir(parents=True, exist_ok=True)
        
        categories = ['pneuma', 'psyche', 'soma', 'opus', 'kismet']
        json_files = {}
        
        for category in categories:
            # Extract data for this category
            category_data = []
            for _, row in df.iterrows():
                category_entry = {
                    'timestamp': row['timestamp'],
                    'log': row[f'{category}.log'],
                    'score': int(row[f'{category}.score'])
                }
                category_data.append(category_entry)
            
            # Save category JSON file
            json_file = os.path.join(output_folder, f"{category}_data.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(category_data, f, indent=2, ensure_ascii=False)
            
            json_files[category] = json_file
            print(f"✓ Created {json_file} with {len(category_data)} records")
        
        return json_files
        
    except Exception as e:
        print(f"✗ Error in csv_to_json_by_category: {e}")
        return {}

def json_by_category_to_csv(json_folder='json_data', output_csv='combined_timeline.csv'):
    """
    Convert category JSON files back to a combined CSV
    
    Args:
        json_folder (str): Folder containing category JSON files
        output_csv (str): Output CSV file path
    
    Returns:
        str: Path to created CSV file
    """
    try:
        categories = ['pneuma', 'psyche', 'soma', 'opus', 'kismet']
        all_data = {}
        
        # Read all category JSON files
        for category in categories:
            json_file = os.path.join(json_folder, f"{category}_data.json")
            if os.path.exists(json_file):
                with open(json_file, 'r', encoding='utf-8') as f:
                    category_data = json.load(f)
                all_data[category] = category_data
                print(f"✓ Loaded {json_file} with {len(category_data)} records")
            else:
                print(f"⚠ Warning: {json_file} not found")
                all_data[category] = []
        
        # Check if we have data
        if not any(all_data.values()):
            print("✗ No data found in any JSON files")
            return None
        
        # Reconstruct CSV data
        csv_data = []
        timestamps = set()
        
        # Collect all timestamps
        for category_data in all_data.values():
            for entry in category_data:
                timestamps.add(entry['timestamp'])
        
        # Convert to sorted list
        timestamps = sorted(list(timestamps))
        
        # Reconstruct rows
        for timestamp in timestamps:
            row = {'timestamp': timestamp}
            
            for category in categories:
                # Find entry for this timestamp and category
                category_entry = None
                for entry in all_data[category]:
                    if entry['timestamp'] == timestamp:
                        category_entry = entry
                        break
                
                if category_entry:
                    row[f'{category}.log'] = category_entry['log']
                    row[f'{category}.score'] = category_entry['score']
                else:
                    row[f'{category}.log'] = ''
                    row[f'{category}.score'] = ''
            
            csv_data.append(row)
        
        # Create DataFrame and save CSV
        df = pd.DataFrame(csv_data)
        
        # Ensure output directory exists
        Path(os.path.dirname(output_csv)).mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output_csv, index=False)
        print(f"✓ Created combined CSV: {output_csv} with {len(df)} records")
        
        return output_csv
        
    except Exception as e:
        print(f"✗ Error in json_by_category_to_csv: {e}")
        return None

def list_files_in_folder(folder='.'):
    """List all CSV and JSON files in a folder"""
    csv_files = glob.glob(os.path.join(folder, "*.csv"))
    json_files = glob.glob(os.path.join(folder, "*.json"))
    
    print(f"\nFiles in {folder}:")
    print("CSV files:")
    for file in csv_files:
        print(f"  📊 {os.path.basename(file)}")
    
    print("JSON files:")
    for file in json_files:
        print(f"  📄 {os.path.basename(file)}")
    
    return {'csv': csv_files, 'json': json_files}

# Example usage and testing
if __name__ == "__main__":
    # Create sample data first if it doesn't exist
    sample_csv = 'timeline_data.csv'
    if not os.path.exists(sample_csv):
        print("Creating sample timeline data...")
        from datetime import datetime, timedelta
        from faker import Faker
        import random
        
        fake = Faker()
        categories = ['pneuma', 'psyche', 'soma', 'opus', 'kismet']
        
        data = []
        start_date = datetime.now() - timedelta(days=19)
        
        for day in range(20):
            current_date = (start_date + timedelta(days=day)).strftime('%Y-%m-%d')
            row = {'timestamp': current_date}
            
            for category in categories:
                row[f'{category}.log'] = fake.sentence(nb_words=6)
                row[f'{category}.score'] = random.randint(0, 100)
            
            data.append(row)
        
        df = pd.DataFrame(data)
        df.to_csv(sample_csv, index=False)
        print(f"✓ Created sample data: {sample_csv}")

    # List current files
    list_files_in_folder()

    # Test 1: Convert CSV to JSON (all files in current folder)
    print("\n" + "="*50)
    print("TEST 1: Converting all CSV files to JSON")
    print("="*50)
    json_files = csv_to_json()
    
    # Test 2: Convert specific CSV to category JSON files
    print("\n" + "="*50)
    print("TEST 2: Converting timeline CSV to category JSON files")
    print("="*50)
    category_files = csv_to_json_by_category('timeline_data.csv', 'category_json')
    
    # Test 3: Convert JSON back to CSV
    print("\n" + "="*50)
    print("TEST 3: Converting JSON files back to CSV")
    print("="*50)
    csv_files = json_to_csv('category_json', 'converted_csv')
    
    # Test 4: Convert category JSON back to combined CSV
    print("\n" + "="*50)
    print("TEST 4: Converting category JSON back to combined CSV")
    print("="*50)
    combined_csv = json_by_category_to_csv('category_json', 'final_combined/timeline_restored.csv')
    
    # Show final file structure
    print("\n" + "="*50)
    print("FINAL FILE STRUCTURE")
    print("="*50)
    for folder in ['.', 'category_json', 'converted_csv', 'final_combined']:
        if os.path.exists(folder):
            list_files_in_folder(folder)

    # Quick verification
    print("\n" + "="*50)
    print("DATA VERIFICATION")
    print("="*50)
    if os.path.exists('timeline_data.csv') and os.path.exists('final_combined/timeline_restored.csv'):
        original = pd.read_csv('timeline_data.csv')
        restored = pd.read_csv('final_combined/timeline_restored.csv')
        
        print(f"Original data shape: {original.shape}")
        print(f"Restored data shape: {restored.shape}")
        print(f"Data matches: {original.shape == restored.shape}")

"""

Files in .:
CSV files:
  📊 timeline_data.csv
JSON files:
  📄 opus_data.json
  📄 soma_data.json
  📄 pneuma_data.json
  📄 psyche_data.json
  📄 kismet_data.json

==================================================
TEST 1: Converting all CSV files to JSON
==================================================
✓ Converted ./timeline_data.csv -> ./timeline_data.json (20 records)

==================================================
TEST 2: Converting timeline CSV to category JSON files
==================================================
✓ Created category_json/pneuma_data.json with 20 records
✓ Created category_json/psyche_data.json with 20 records
✓ Created category_json/soma_data.json with 20 records
✓ Created category_json/opus_data.json with 20 records
✓ Created category_json/kismet_data.json with 20 records

==================================================
TEST 3: Converting JSON files back to CSV
==================================================
✓ Converted category_json/opus_data.json -> converted_csv/opus_data.csv (20 records)
✓ Converted category_json/soma_data.json -> converted_csv/soma_data.csv (20 records)
✓ Converted category_json/pneuma_data.json -> converted_csv/pneuma_data.csv (20 records)
✓ Converted category_json/psyche_data.json -> converted_csv/psyche_data.csv (20 records)
✓ Converted category_json/kismet_data.json -> converted_csv/kismet_data.csv (20 records)

==================================================
TEST 4: Converting category JSON back to combined CSV
==================================================
✓ Loaded category_json/pneuma_data.json with 20 records
✓ Loaded category_json/psyche_data.json with 20 records
✓ Loaded category_json/soma_data.json with 20 records
✓ Loaded category_json/opus_data.json with 20 records
✓ Loaded category_json/kismet_data.json with 20 records
✓ Created combined CSV: final_combined/timeline_restored.csv with 20 records

==================================================
FINAL FILE STRUCTURE
==================================================

Files in .:
CSV files:
  📊 timeline_data.csv
JSON files:
  📄 opus_data.json
  📄 soma_data.json
  📄 pneuma_data.json
  📄 psyche_data.json
  📄 kismet_data.json
  📄 timeline_data.json

Files in category_json:
CSV files:
JSON files:
  📄 opus_data.json
  📄 soma_data.json
  📄 pneuma_data.json
  📄 psyche_data.json
  📄 kismet_data.json

Files in converted_csv:
CSV files:
  📊 soma_data.csv
  📊 kismet_data.csv
  📊 psyche_data.csv
  📊 opus_data.csv
  📊 pneuma_data.csv
JSON files:

Files in final_combined:
CSV files:
  📊 timeline_restored.csv
JSON files:

==================================================
DATA VERIFICATION
==================================================
Original data shape: (20, 11)
Restored data shape: (20, 11)
Data matches: True
"""        