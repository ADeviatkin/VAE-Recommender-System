from sqlalchemy import create_engine, text
import pandas as pd
import os
import json

# Setup database connection
db_connection_string = 'sqlite:///db.db'
engine = create_engine(db_connection_string)

# Define folders containing data files
business_info_folder = '/model_related/filtered_meta_data'
business_ratings_folder = '/model_related/filtered_ratings_USA'

def create_table_if_not_exists(state, is_ratings=False):
    """Create the table if it does not exist."""
    table_name = f'business_info_{state}' if not is_ratings else f'business_ratings_{state}'
    if is_ratings:
        sql = f"""
        CREATE TABLE IF NOT EXISTS "{table_name}" (
            rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
            gmap_id TEXT,
            user_id TEXT,
            rating REAL,
            timestamp INTEGER,
            FOREIGN KEY(gmap_id) REFERENCES "{table_name}"(gmap_id)
        );
        """
    else:
        sql = f"""
        CREATE TABLE IF NOT EXISTS "{table_name}" (
            gmap_id TEXT PRIMARY KEY,
            name TEXT,
            address TEXT,
            description TEXT,
            latitude REAL,
            longitude REAL,
            category TEXT,
            avg_rating REAL,
            num_of_reviews INTEGER,
            price TEXT
        );
        """
    with engine.begin() as conn:
        conn.execute(text(sql))

def bulk_insert_business_info(state, records):
    """Bulk insert or update business info records."""
    table_name = f'business_info_{state}'
    insert_sql = text(f"""
    INSERT INTO "{table_name}" (gmap_id, name, address, description, latitude, longitude, category, avg_rating, num_of_reviews, price)
    VALUES (:gmap_id, :name, :address, :description, :latitude, :longitude, :category, :avg_rating, :num_of_reviews, :price)
    ON CONFLICT(gmap_id) DO UPDATE SET
    name=excluded.name,
    address=excluded.address,
    description=excluded.description,
    latitude=excluded.latitude,
    longitude=excluded.longitude,
    category=excluded.category,
    avg_rating=excluded.avg_rating,
    num_of_reviews=excluded.num_of_reviews,
    price=excluded.price;
    """)

    with engine.begin() as conn:
        conn.execute(insert_sql, records)

def import_business_info(state, file_path):
    """Import business info from JSON file."""
    create_table_if_not_exists(state)
    records = []
    with open(file_path, 'r') as file:
        for line in file:
            record = json.loads(line)
            record['category'] = ','.join(record.get('category', []))
            for key in ['hours', 'MISC', 'relative_results', 'state', 'url']:
                record.pop(key, None)
            records.append(record)
    if records:
        bulk_insert_business_info(state, records)
    print(f"Imported {file_path} into {state}.")

def import_business_ratings(state, file_path):
    """Import business ratings from CSV file."""
    create_table_if_not_exists(state, is_ratings=True)
    df = pd.read_csv(file_path)
    df.rename(columns={'business': 'gmap_id', 'user': 'user_id'}, inplace=True)
    table_name = f'business_ratings_{state}'
    df.to_sql(table_name, con=engine, if_exists='append', index=False, method='multi')
    print(f"Imported {file_path} into {state}.")

# Import data from files
for filename in os.listdir(business_info_folder):
    if filename.endswith('.json'):
        state_name = filename.split('-')[1].replace('.json', '').lower()
        file_path = os.path.join(business_info_folder, filename)
        import_business_info(state_name, file_path)
"""
for filename in os.listdir(business_ratings_folder):
    if filename.endswith('.csv'):
        state_name = filename.split('-')[1].replace('.csv', '').lower()
        file_path = os.path.join(business_ratings_folder, filename)
        import_business_ratings(state_name, file_path)
"""
print("Data import complete.")