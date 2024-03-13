import numpy as np
import torch
from recbole.config import Config
from recbole.data import create_dataset, data_preparation
from recbole.model.general_recommender import MultiVAE, RecVAE
from recbole.utils import init_seed, ensure_dir
import os

# Path to model
model_save_path = './saved_last/RecVAE-Wyoming.pth'
checkpoint = torch.load(model_save_path, map_location=torch.device('cpu'))
print("Available keys in checkpoint:", checkpoint.keys())
config_dict = checkpoint['config']
loaded_config = Config(model=config_dict['model'], dataset=config_dict['dataset'])

dataset = create_dataset(loaded_config)
_, _, test_data = data_preparation(loaded_config, dataset)

model = RecVAE(loaded_config, test_data.dataset).to(loaded_config['device'])
model.load_state_dict(checkpoint['state_dict'])
model.eval()

def simulate_new_user_interaction_vector(dataset, new_reviews):
    """
    Create a user interaction vector for a new user based on their reviews.
    
    Args:
        dataset: The loaded dataset, to know the number of items.
        new_reviews: A dictionary with item IDs as keys and review values (e.g., ratings) as values.
        
    Returns:
        A numpy array representing the user's interaction vector.
    """
    interaction_vector = np.zeros(dataset.item_num)
    
    for item_id, rating in new_reviews.items():
        item_index = dataset.token2id(dataset.iid_field, item_id)
        interaction_vector[item_index] = rating
    
    return interaction_vector
def generate_recommendations_for_new_user(model, interaction_vector, top_k=10, dropout_prob=0.5):
    """
    Generate recommendations for a new user based on their interaction vector.

    Args:
        model: The trained RecVAE model.
        interaction_vector: The user's interaction vector as a numpy array.
        top_k: Number of top recommendations to generate.
        dropout_prob: The dropout probability to use during inference (likely 0 for no dropout).

    Returns:
        A list of top-k recommended item IDs.
    """
    interaction_tensor = torch.FloatTensor(interaction_vector).to(model.device).unsqueeze(0)
    
    with torch.no_grad():
        reconstructed_vector = model(interaction_tensor, dropout_prob)[0].squeeze(0)
        _, top_k_indices = torch.topk(reconstructed_vector, k=top_k)
    
    top_k_item_ids = [dataset.id2token(dataset.iid_field, idx.item()) for idx in top_k_indices]
    
    return top_k_item_ids

# Example new user reviews: {'item_id1': rating1, 'item_id2': rating2, ...}
new_reviews = {
    '0x534c1eda79c33d4d:0xd2b80eb61a03565': 5,
    '0x534c1eda79c33d4d:0xd2b80eb61a03565': 4,
    # Add more as needed
}

interaction_vector = simulate_new_user_interaction_vector(dataset, new_reviews)

new_user_recommendations = generate_recommendations_for_new_user(model, interaction_vector, top_k=10)
print(f"Recommendations for new user: {new_user_recommendations}")
