import os
import matplotlib.pyplot as plt
from glob import glob

folder_path = './filtered_ratings_USA'  # Path to the folder with CSV files


output_folder_path = './plots' # Path to the folder where the plots will be saved

if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

for file_path in glob(os.path.join(folder_path, '*.csv')):
    print(f"In progress: {file_path}")
    
    reviews = []
    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            reviews.append(line.strip())

    user_review_count = {}
    for review in reviews:
        _, user_id, _, _ = review.split(',')
        if user_id in user_review_count:
            user_review_count[user_id] += 1
        else:
            user_review_count[user_id] = 1

    review_categories = {1: 0, 2: 0, 3: 0, 4: 0, '5+': 0}
    for count in user_review_count.values():
        if count > 4:
            review_categories['5+'] += 1
        else:
            review_categories[count] += 1

    updated_labels = ['1 review', '2 reviews', '3 reviews', '4 reviews', '5+ reviews']
    values = list(review_categories.values())

    plt.figure(figsize=(7, 6))
    plt.pie(values, labels=updated_labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors, textprops={'fontsize': 14})
    plt.axis('equal') 
    
    file_name = os.path.basename(file_path).replace('.csv', '.png')
    save_path = os.path.join(output_folder_path, file_name)
    plt.savefig(save_path)
    plt.close()
    print(f"Saved to: {save_path}")
