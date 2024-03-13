from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from sqlalchemy import create_engine, text
import numpy as np

from recbole.config import Config
from recbole.data import create_dataset, data_preparation
from recbole.model.general_recommender import RecVAE
from recbole.utils import init_seed, ensure_dir
from src.recommendation_service import get_recommendations
app = Flask(__name__)
CORS(app)

db_connection_string = 'sqlite:///db/db.db'
engine = create_engine(db_connection_string)
@app.route('/api/ratings/user/<user_id>', methods=['GET'])
def get_user_ratings(user_id):
    query = """
        SELECT * FROM user_ratings WHERE user_id = :user_id
    """
    df = pd.read_sql(query, con=engine, params={"user_id": user_id})
    return jsonify(df.to_dict(orient="records"))

@app.route('/api/placesfilter', methods=['GET'])
def get_places_by_filter():
    user_id = request.args.get('user_id', default="user123", type=str)
    name_filter = request.args.get('name', default='', type=str)
    state_filter = request.args.get('state', default='', type=str)
    category_filter = request.args.get('category', default=None, type=str)
    page = request.args.get('page', default=1, type=int)
    items_per_page = 10
    offset = (page - 1) * items_per_page
    if not state_filter:
        return None
    query = """
        SELECT b.*, r.rating
        FROM business_info_"""+state_filter+""" b
        LEFT JOIN user_ratings r ON b.gmap_id = r.gmap_id AND r.user_id = :user_id
        WHERE 1=1
    """
    if name_filter:
        query += f" AND b.name LIKE '%{name_filter}%'"
    if category_filter:
        query += f" AND b.category = '{category_filter}'"
    query += f" ORDER BY b.name LIMIT {items_per_page} OFFSET {offset}"
    df = pd.read_sql(query, con=engine, params={"user_id": user_id})
    df = df.where(pd.notnull(df), None)
    df.replace({np.nan: -1}, inplace=True)
    return jsonify(df.to_dict(orient="records"))

@app.route('/api/rate', methods=['POST'])
def submit_rating():
    print("submit_rating: ", request.json)
    sql_command = text("""
    INSERT INTO user_ratings (gmap_id, user_id, rating)
    VALUES (:gmap_id, :user_id, :rating)
    ON CONFLICT(gmap_id, user_id) 
    DO UPDATE SET rating = :rating
    """) 

    with engine.begin() as connection:
        result = connection.execute(sql_command, request.json)
    return jsonify({"message": "Rating submitted successfully"}), 200


@app.route('/api/recommendations', methods=['GET'])
def recommendations():
    user_id = request.args.get('user_id', default='user123', type=str)
    state = request.args.get('state', default=None, type=str)

    if not state:
        return jsonify({"error": "State parameter is required."}), 400

    allowed_states = ['Alabama', 'Wyoming', 'Maine']  # States with prepared models
    if state not in allowed_states:
        return jsonify({"error": "Invalid state provided."}), 400

    state_table = state.replace(" ", "_").lower()

    user_ratings_query = f"""
        SELECT ur.gmap_id, ur.rating 
        FROM user_ratings ur
        JOIN business_info_{state_table} bi ON ur.gmap_id = bi.gmap_id
        WHERE ur.user_id = :user_id
    """
    user_ratings_df = pd.read_sql(user_ratings_query, con=engine, params={"user_id": user_id})
    
    new_reviews = user_ratings_df.set_index('gmap_id')['rating'].to_dict()
    recommendation_ids = get_recommendations(state, new_reviews)

    if not recommendation_ids:
        return jsonify({"error": "No recommendations found."}), 404

    named_placeholders = [f":gmap_id_{i}" for i in range(len(recommendation_ids))]
    placeholders_str = ', '.join(named_placeholders)

    business_info_query = f"""
        SELECT b.*, r.rating
        FROM business_info_{state_table} b
        LEFT JOIN user_ratings r ON b.gmap_id = r.gmap_id AND r.user_id = :user_id
        WHERE b.gmap_id IN ({placeholders_str})
    """

    params = {"user_id": user_id}
    params.update({f"gmap_id_{i}": recommendation_id for i, recommendation_id in enumerate(recommendation_ids)})

    df = pd.read_sql(business_info_query, con=engine, params=params)

    if df.empty:
        return jsonify({"error": "No business information found for recommendations."}), 404

    df = df.where(pd.notnull(df), -1)

    return jsonify(df.to_dict(orient="records"))

    
@app.route('/api/validate_user_id', methods=['POST'])
def validate_user_id():
    user_id = request.json.get('user_id')
    valid_user_ids = ['user123']
    
    if user_id in valid_user_ids:
        return jsonify({"valid": True}), 200
    else:
        return jsonify({"valid": False, "message": "Invalid user ID"}), 400

if __name__ == '__main__':
    app.run(debug=True)

