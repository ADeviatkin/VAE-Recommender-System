import json
import csv
import os

# Directories to data
ratings_folder = './filtered_ratings_USA_choosen'
metadata_folder = './filtered_meta_data_choosen'

# Define output filenames
output_items_file = '.item'
output_users_file = '.user'
output_interactions_file = '.inter'

# Define headers for the output files
item_headers = ['item_id:token', 'category:token', 'avg_rating:float', 'num_of_reviews:int', 'has_description:bool']
user_headers = ['user_id:token']
inter_headers = ['user_id:token', 'item_id:token', 'rating:float', 'timestamp:float']

def clean_string(input_string):
    return input_string[0].replace('\x00', '').replace('\n', '').replace('\r', '') if input_string else input_string

def item_has_no_none(meta_data):
    return all(meta_data.get(field) is not None for field in ['name', 'address', 'category', 'avg_rating', 'num_of_reviews'])

item_metadata = {}
for filename in os.listdir(metadata_folder):
    if filename.startswith('meta-') and filename.endswith('.json'):
        with open(os.path.join(metadata_folder, filename), 'r', encoding='utf-8') as file:
            for line in file:
                meta_data = json.loads(line)
                gmap_id = meta_data['gmap_id']
                if item_has_no_none(meta_data): 
                    item_metadata[gmap_id] = meta_data

items_data = []
users = set()
interactions_data = []

# Define how split data
#item_metadata = {gmap_id: meta_data for gmap_id, meta_data in item_metadata.items() if meta_data['num_of_reviews'] <500}

# Define user data to store
for filename in os.listdir(ratings_folder):
    if filename.startswith('rating-') and filename.endswith('.csv'):
        with open(os.path.join(ratings_folder, filename), 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader) 
            for row in csv_reader:
                business_id, user_id, rating, timestamp = row
                if business_id in item_metadata:
                    users.add(user_id)
                    interactions_data.append({
                        'user_id:token': user_id,
                        'item_id:token': business_id,
                        'rating:float': rating,
                        'timestamp:float': timestamp,
                    })

# Define business data to store
for gmap_id, meta_data in item_metadata.items():
    items_data.append({
        'item_id:token': gmap_id,
        'name:token': clean_string(meta_data['name']),
        #'address:token': clean_string(meta_data['address']),
        #'category:token': clean_string(meta_data['category']),
        'avg_rating:float': str(meta_data['avg_rating']),
        'num_of_reviews:int': str(meta_data['num_of_reviews']),
        'has_description:bool': '1' if meta_data.get('description') else '0'
    })


def write_to_recbole_file(filename, headers, data):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers, delimiter='\t')
        writer.writeheader()
        for row in data:
            cleaned_row = {k: v for k, v in row.items() if k in headers}
            writer.writerow(cleaned_row)

write_to_recbole_file(output_items_file, item_headers, items_data)
write_to_recbole_file(output_users_file, user_headers, [{'user_id:token': user} for user in users])
write_to_recbole_file(output_interactions_file, inter_headers, interactions_data)

print("Data processing complete. Files are ready for RecBole.")