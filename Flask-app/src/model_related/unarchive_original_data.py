import os
import gzip
import shutil

def unarchive_folder(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    for filename in os.listdir(source_dir):
        if filename.endswith('.gz'):
            gz_path = os.path.join(source_dir, filename)
            unarchived_path = os.path.join(target_dir, filename[:-3])
            
            with gzip.open(gz_path, 'rb') as f_in:
                with open(unarchived_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

# Define the source and target directories
source_dirs = ['meta_USA', 'ratings_USA']
target_dirs = ['meta_USA_unarchived', 'ratings_USA_unarchived']

for source_dir, target_dir in zip(source_dirs, target_dirs):
    unarchive_folder(source_dir, target_dir)
