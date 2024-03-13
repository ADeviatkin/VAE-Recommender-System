import os
import json
from collections import Counter

def count_categories_in_files(directory):
    category_counts = Counter()
    
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    try:
                        data = json.loads(line)
                        categories = data.get("category", [])
                        category_counts.update(categories)
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in file {filename} on line: {line}")
    
    return category_counts

directory = './meta_USA_unarchived' # Directory to meta data
output_file = './category_counts_sorted_by_count.txt' # File to store output

categories_count = count_categories_in_files(directory)
sorted_categories = sorted(categories_count.items(), key=lambda x: x[1], reverse=True)

with open(output_file, 'w', encoding='utf-8') as f:
    for category, count in sorted_categories:
        f.write(f"{category}: {count}\n")

print(f"Category counts have been saved to {output_file}, sorted by count in descending order.")
