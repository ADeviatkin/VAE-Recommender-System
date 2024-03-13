import os
import json
from collections import Counter

def filter_and_recount_categories(source_directory, target_directory, count_file):
    category_counts = Counter()
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    
    for filename in os.listdir(source_directory):
        if filename.endswith('.json'):
            source_path = os.path.join(source_directory, filename)
            target_path = os.path.join(target_directory, filename)
            
            with open(source_path, 'r', encoding='utf-8') as file, open(target_path, 'w', encoding='utf-8') as outfile:
                for line in file:
                    data = json.loads(line)
                    categories = data.get("category")
                    if not isinstance(categories, list):
                        categories = []
                    new_categories = []
                    for category in categories:
                        if "restaurant" in category.lower():
                            new_categories.append("restaurant")
                            category_counts.update(["restaurant"])
                            break
                        elif "bar" in category.lower():
                            new_categories.append("bar")
                            category_counts.update(["bar"])
                            break
                        elif "pub" in category.lower():
                            new_categories.append("pub")
                            category_counts.update(["pub"])
                            break
                    if new_categories:
                        data["category"] = new_categories
                        json.dump(data, outfile)
                        outfile.write('\n')
    
    count_path = os.path.join(target_directory, count_file)
    with open(count_path, 'w', encoding='utf-8') as f:
        for category, count in category_counts.items():
            f.write(f"{category}: {count}\n")

source_directory = './meta_USA_unarchived' # Directory containing original meta data
target_directory = './filtered_meta_data' # Directory to for output
count_file = './category_counts.txt' # Directory to meta data

filter_and_recount_categories(source_directory, target_directory, count_file)

print(f"Processed data has been saved to {target_directory}, and category counts to {count_file}.")
