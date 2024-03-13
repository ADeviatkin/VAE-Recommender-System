import json
import torch
import numpy as np
from recbole.config import Config
from recbole.data import create_dataset, data_preparation
from recbole.model.general_recommender import RecVAE
from sqlalchemy import create_engine
import pandas as pd

# path to config file
models_config_path = './src/model_related/train_model/saved_last/models_config.json'
db_connection_string = 'sqlite:///db/db.db'
engine = create_engine(db_connection_string)

def load_models(state):
    with open(models_config_path, 'r') as f:
        models_config = json.load(f)
    state_configs = models_config.get(state, {})
    models = {}
    for model_key, model_info in state_configs.items():
        model_path = model_info['model_path']
        checkpoint = torch.load(model_path, map_location=torch.device('cpu'))
        config_dict = checkpoint['config']
        loaded_config = Config(model=config_dict['model'], dataset=config_dict['dataset'])
        dataset = create_dataset(loaded_config)
        _, _, test_data = data_preparation(loaded_config, dataset)
        model = RecVAE(loaded_config, test_data.dataset).to(loaded_config['device'])
        model.load_state_dict(checkpoint['state_dict'])
        model.eval()
        models[model_key] = {'model': model, 'dataset': dataset, 'info': model_info}
    return models

def simulate_new_user_interaction_vector(dataset, new_reviews):
    interaction_vector = np.zeros(dataset.item_num)
    for item_id, rating in new_reviews.items():
        item_index = dataset.token2id(dataset.iid_field, item_id)
        if item_index is not None:
            interaction_vector[item_index] = rating
    return interaction_vector

def generate_recommendations_for_new_user(model, dataset, interaction_vector, top_k=10, dropout_prob=0.5):
    interaction_tensor = torch.FloatTensor(interaction_vector).to(model.device).unsqueeze(0)
    with torch.no_grad():
        reconstructed_vector = model(interaction_tensor, dropout_prob)[0].squeeze(0)
        _, top_k_indices = torch.topk(reconstructed_vector, k=top_k)
    top_k_item_ids = [dataset.id2token(dataset.iid_field, idx.item()) for idx in top_k_indices]
    return top_k_item_ids

def get_business_reviews(state, business_ids):
    df = pd.read_sql(f"SELECT gmap_id, num_of_reviews FROM business_info_{state} WHERE gmap_id IN ({','.join(['?']*len(business_ids))})", engine, params=tuple(business_ids))
    return df.set_index('gmap_id')['num_of_reviews'].to_dict()


def get_recommendations(state, user_reviews):
    models = load_models(state)
    all_recommendations = []
    business_ids = list(user_reviews.keys())
    business_reviews = get_business_reviews(state, business_ids)
    for model_key, model_info in models.items():
        applicable_reviews = {gmap_id: rating for gmap_id, rating in user_reviews.items() if gmap_id in business_ids and business_reviews.get(gmap_id, 0) >= model_info['info'].get('reviews_threshold', 0)}
        if not applicable_reviews:
            continue
        interaction_vector = simulate_new_user_interaction_vector(model_info['dataset'], applicable_reviews)
        recommendations = generate_recommendations_for_new_user(model_info['model'], model_info['dataset'], interaction_vector, top_k=10)
        all_recommendations.extend(recommendations)
    top_k_adjusted = len(all_recommendations)
    return all_recommendations[:top_k_adjusted]