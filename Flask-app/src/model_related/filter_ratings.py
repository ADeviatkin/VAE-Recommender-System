import csv
import json
import os

def extract_business_ids_from_json(directory):
    business_ids = set()
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                for line in file:
                    data = json.loads(line)
                    business_ids.add(data['gmap_id'])
    return business_ids

def filter_csv_reviews(source_csv_directory, target_csv_directory, business_ids):
    if not os.path.exists(target_csv_directory):
        os.makedirs(target_csv_directory)
    
    for filename in os.listdir(source_csv_directory):
        if filename.endswith('.csv'):
            input_path = os.path.join(source_csv_directory, filename)
            output_path = os.path.join(target_csv_directory, filename)
            
            with open(input_path, mode='r', encoding='utf-8') as infile, \
                 open(output_path, mode='w', encoding='utf-8', newline='') as outfile:
                reader = csv.DictReader(infile)
                writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
                writer.writeheader()
                
                for row in reader:
                    if row['business'] in business_ids:
                        writer.writerow(row)

json_directory = './filtered_meta_data' # Directory to meta data
source_csv_directory = './ratings_USA_unarchived'  # Directory containing original CSV files
target_csv_directory = './filtered_ratings_USA'  # Directory where filtered CSV files will be saved

business_ids = extract_business_ids_from_json(json_directory)

filter_csv_reviews(source_csv_directory, target_csv_directory, business_ids)

print("Reviews have been filtered based on the businesses listed in the JSON files.")
