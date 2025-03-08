import pickle
import pandas as pd
from sklearn.linear_model import LinearRegression

MODEL_PATH = "model.pkl"

def train_model(data):
    """Train a regression model with the provided data."""
    df = pd.DataFrame(data)
    X = df.drop('target', axis=1)
    y = df['target']
    model = LinearRegression()
    model.fit(X, y)
    return model

def save_model(model):
    """Save the trained model to a file."""
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)

def load_model():
    """Load the model from a file."""
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        print("Model file not found.")
        return None

def predict(model, data):
    """Make predictions using the trained model."""
    df = pd.DataFrame(data)
    predictions = model.predict(df)
    return predictions.tolist() 