import pandas as pd
from model import train_model, save_model, load_model, predict
import requests

# Load synthetic data from an ODS file
def load_synthetic_data(file_path='Synthetic-data.ods', sheet_name='Sheet1'):
    # Read the ODS file
    data = pd.read_excel(file_path, sheet_name=sheet_name, engine='odf')
    return data

# Test the train and predict functions
def test_model():
    # Load synthetic data
    data = load_synthetic_data()

    # Ensure the data has the necessary columns
    required_columns = [
        'Local Authority', 
        'Projected ROI (%)', 
        'EV Adoption Rate (%)', 
        'Projected EV Growth (%)', 
        'Regulatory Complexity Score', 
        'Investment Feasibility Score',  # Assuming this is the target
        'EV Chargers'  # Ensure this column exists
    ]
    if not all(column in data.columns for column in required_columns):
        print("Data does not contain the required columns.")
        return

    # Map the columns to the expected feature names
    data = data.rename(columns={
        'Projected ROI (%)': 'cost',
        'EV Adoption Rate (%)': 'demand',
        'Projected EV Growth (%)': 'demand_growth',
        'Regulatory Complexity Score': 'regulatory',
        'Investment Feasibility Score': 'target'  # Assuming this is the target
    })

    # Combine demand features into a single 'demand' feature
    data['demand'] = data[['demand', 'demand_growth']].mean(axis=1)

    # Drop the extra demand growth column
    data = data.drop(columns=['demand_growth'])

    # Select only numeric columns for training
    feature_columns = ['cost', 'demand', 'regulatory']
    X = data[feature_columns]
    y = data['target']

    # Train the model
    model = train_model(pd.concat([X, y], axis=1))

    # Save the model
    save_model(model)
    print("Model trained and saved successfully.")

    # Load the model
    loaded_model = load_model()
    if loaded_model is None:
        print("Failed to load the model.")
        return

    # Prepare data for prediction (without target)
    prediction_data = X

    # Make predictions
    predictions = predict(loaded_model, prediction_data)

    # Display predictions by Local Authority
    results = pd.DataFrame({
        'Local Authority': data['Local Authority'],
        'Prediction': predictions
    })

    # Simulate API calls
    chargers_info = simulate_chargers_api(data)
    feasibility_info = simulate_feasibility_api(data)
    underserved_info = simulate_underserved_api(data)

    # Add API results to the DataFrame
    results['Chargers'] = chargers_info
    results['Feasibility'] = feasibility_info
    results['Underserved'] = underserved_info

    print(results.head())  # Display the first few results

def simulate_chargers_api(data):
    # Simulate the /chargers API call
    return data['EV Chargers'].tolist()

def simulate_feasibility_api(data):
    # Simulate the /feasibility API call
    feasibility_scores = []
    for _, row in data.iterrows():
        score = (row['cost'] * 0.3) + (row['demand'] * 0.4) + (row['regulatory'] * 0.3)
        feasibility_scores.append(score)
    return feasibility_scores

def simulate_underserved_api(data, threshold=5):
    # Simulate the /underserved API call
    return (data['EV Chargers'] < threshold).tolist()

if __name__ == "__main__":
    test_model() 