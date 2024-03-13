# Full Stack Flask-React Application

This repository contains a full-stack application with a Flask backend and React frontend, designed to showcase a recommendation system using VAEs.

## Setup Instructions

### Backend Setup

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd path/to/Flask-app
    ```

2. **Create a Python Virtual Environment**:
    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment**:
      ```bash
      source venv/bin/activate
      ```

4. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Set up the Database**:
    ```bash
    python create_database.py
    ```

6. **Run the Flask Application**:
    ```bash
    flask run
    ```
    or
    ```bash
    python app.py
    ```

### Frontend Setup

1. **Navigate to the React App Directory**:
    ```bash
    cd path/to/React-app
    ```

2. **Install npm Packages**:
    ```bash
    npm install
    ```

3. **Start the React Application**:
    ```bash
    npm start
    ```

The React application will open in your default web browser, connecting to the Flask backend automatically.

## Using the Application

- **Frontend**: The React app provides a user interface for interacting with the recommendation system. Navigate through the app to view and rate places, receiving personalized recommendations based on your preferences.
- **Backend**: The Flask app handles requests from the frontend, interacts with the database, and employs a recommendation algorithm to provide personalized place recommendations.

