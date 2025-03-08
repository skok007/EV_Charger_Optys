from flask import Flask, jsonify, request
from my_flask_app.model import train_model, save_model, load_model, predict
import os

# Initialize Flask application
app = Flask(__name__)

# Load model on startup
model = load_model()

@app.route('/')
def home():
    """Home route to check API status."""
    return jsonify({"message": "EV Charging Investment API is running"})

@app.route('/train', methods=['POST'])
def train():
    """Endpoint to train the model."""
    data = request.get_json()
    model = train_model(data)
    save_model(model)
    return jsonify({"message": "Model trained and saved successfully."})

@app.route('/predict', methods=['POST'])
def make_prediction():
    """Endpoint to make predictions using the trained model."""
    # Check if the model is loaded at the time of prediction
    current_model = load_model()
    if current_model is None:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()
    try:
        prediction = predict(current_model, data)
        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Configure host and port dynamically from environment variables
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")  # Default to 0.0.0.0 for external access
    port = int(os.getenv("FLASK_RUN_PORT", 5001))  # Default port to 5000
    app.run(debug=True, host=host, port=port) 