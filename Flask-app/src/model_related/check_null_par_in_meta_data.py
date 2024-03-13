import os
import json
from collections import defaultdict

# Paths to the directory and output file
directory = './filtered_meta_data'
output_file = './complete_counts.txt'

total_count = 0
missing_data_counts = defaultdict(int)

def check_all_fields(entry):
    for key, value in entry.items():
        if value is None or value == '':
            missing_data_counts[key] += 1

for filename in os.listdir(directory):
    if filename.endswith('.json'):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                data = json.loads(line)
                total_count += 1
                check_all_fields(data)

with open(output_file, 'w', encoding='utf-8') as file:
    file.write(f"Total number of businesses: {total_count}\n")
    for field, count in missing_data_counts.items():
        file.write(f"{field} missing: {count}\n")

print(f"Complete counts have been saved to {output_file}.")
