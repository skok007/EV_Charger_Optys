from flask import Flask, jsonify, request
import pandas as pd
import os

# Initialize Flask application
app = Flask(__name__)

# Load dataset from the given file path
file_path = "electric-vehicle-public-charging-infrastructure-statistics-january-2025.ods"
print("Loading dataset from:", file_path)
data = pd.read_excel(file_path, sheet_name="1a")

# Ensure dataset structure is consistent before processing
if len(data) > 2:
    print("Processing dataset with expected structure.")
    columns = data.iloc[1]  # Use second row as column names
    cleaned_data = data[2:].reset_index(drop=True)
    cleaned_data.columns = columns
    cleaned_data = cleaned_data[["Local authority / region name", "Jan-25"]]
    cleaned_data.columns = ["Local Authority", "EV Chargers"]
    # Convert charger count to numeric, handling errors gracefully
    cleaned_data["EV Chargers"] = pd.to_numeric(cleaned_data["EV Chargers"], errors="coerce")
else:
    print("Dataset is empty or has an inconsistent structure. Initializing empty DataFrame.")
    cleaned_data = pd.DataFrame(columns=["Local Authority", "EV Chargers"])

# Load scoring weights from environment variables or use defaults
COST_WEIGHT = float(os.getenv("COST_WEIGHT", 0.3))  # Weight assigned to cost factor
DEMAND_WEIGHT = float(os.getenv("DEMAND_WEIGHT", 0.4))  # Weight assigned to demand factor
REGULATORY_WEIGHT = float(os.getenv("REGULATORY_WEIGHT", 0.3))  # Weight assigned to regulatory factor
print(f"Scoring Weights - Cost: {COST_WEIGHT}, Demand: {DEMAND_WEIGHT}, Regulatory: {REGULATORY_WEIGHT}")

@app.route('/')
def home():
    """Home route to check API status."""
    print("Home endpoint accessed.")
    return jsonify({"message": "EV Charging Investment API is running"})

# Endpoint to get charger availability per local authority with pagination
@app.route('/chargers', methods=['GET'])
def get_chargers():
    """Retrieve a paginated list of charger availability per local authority."""
    print("Fetching charger availability.")
    page = request.args.get("page", 1, type=int)  # Get page number from query params
    per_page = request.args.get("per_page", 10, type=int)  # Get results per page
    print(f"Pagination parameters - Page: {page}, Per Page: {per_page}")
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = cleaned_data.iloc[start:end]
    return jsonify({
        "total_records": len(cleaned_data),
        "page": page,
        "per_page": per_page,
        "data": paginated_data.to_dict(orient='records')
    })

# Endpoint to get underserved areas based on charger availability
@app.route('/underserved', methods=['GET'])
def get_underserved():
    """Retrieve a list of areas with low charger availability based on a threshold."""
    print("Fetching underserved areas.")
    threshold = request.args.get("threshold", 5, type=int)  # Get threshold from query params
    print(f"Threshold set to: {threshold}")
    if threshold < 0:
        print("Invalid threshold value received.")
        return jsonify({"error": "Threshold must be a positive integer."}), 400  # Handle invalid threshold
    underserved = cleaned_data[cleaned_data["EV Chargers"] < threshold]
    return jsonify(underserved.to_dict(orient='records'))

# Endpoint to compute investment feasibility score
@app.route('/feasibility', methods=['POST'])
def calculate_feasibility():
    """Calculate feasibility score based on cost, demand, and regulatory factors."""
    print("Processing feasibility score calculation.")
    data = request.get_json()
    cost = data.get("cost", 1)  # Default cost factor
    demand = data.get("demand", 1)  # Default demand factor
    regulatory = data.get("regulatory", 1)  # Default regulatory factor
    print(f"Received inputs - Cost: {cost}, Demand: {demand}, Regulatory: {regulatory}")
    
    # Calculate feasibility score using weighted parameters
    score = (cost * COST_WEIGHT) + (demand * DEMAND_WEIGHT) + (regulatory * REGULATORY_WEIGHT)
    print(f"Calculated feasibility score: {score}")
    return jsonify({"feasibility_score": score})

if __name__ == '__main__':
    # Configure host and port dynamically from environment variables
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")  # Default to 0.0.0.0 for external access
    port = int(os.getenv("FLASK_RUN_PORT", 5002))  # Default port to 5002
    print(f"Starting Flask application on {host}:{port}")
    app.run(debug=True, host=host, port=port)
