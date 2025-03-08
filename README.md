# EV_Charger_Optys
Model and app to identify areas in UK that are underserved when it comes to EV chargers

## Overview
EV_Charger_Optys is a model and application designed to identify areas in the UK that are underserved when it comes to electric vehicle (EV) chargers. The goal of this project is to provide insights and data to help improve the infrastructure for EV charging, ensuring that all regions have adequate access to charging stations.

## Features
- **Data Analysis**: Analyze various datasets to identify regions with insufficient EV charging infrastructure.
- **Visualization**: Generate visual representations of underserved areas to aid in decision-making.
- **Reporting**: Provide detailed reports on the current state of EV charging infrastructure and recommendations for improvement.

## Installation
To set up the project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/EV_Charger_Optys.git
    cd EV_Charger_Optys
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    python app.py
    ```

## Usage
Once the application is running, you can use the web interface to explore the data and generate reports. The interface allows you to select different regions and view the current state of EV charging infrastructure. Additionally, there is a test suite available to ensure the functionality of the application. Run the tests using:
```bash
python -m unittest discover
```

## Data Source
The data used in this project is based on public data from the UK Department for Transport. You can find the dataset [here](https://findtransportdata.dft.gov.uk/dataset/electric-vehicle-charging-infrastructure-statistics-17eb4e7de79).

## File Structure
- `Flask app/my_flask_app/app.py`: Main Flask application file that defines the API endpoints.
- `Flask app/my_flask_app/model.py`: Contains functions for training, saving, loading, and predicting with the regression model.
- `Flask app/my_flask_app/test.py`: Unit tests for the Flask API endpoints.
- `Flask app/my_flask_app/test_model.py`: Tests for the model training and prediction functions.
- `Flask app/my_flask_app/utils.py`: Utility functions (currently empty).
- `Flask app/Regression.py`: Original file generated using the B.R.I.D.G.E. Framework. 
- `Flask app/electric-vehicle-public-charging-infrastructure-statistics-january-2025.ods`: ODS file containing the dataset.
- `Flask app/Synthetic-data.ods`: ODS file containing synthetic data for testing.
- `Flask app/model.pkl`: Pickle file to save the trained model.
- `Flask app/my_flask_app/requirements.txt`: List of dependencies required for the project.
- `LICENSE`: License file for the project.
- `.gitignore`: Git ignore file to exclude unnecessary files from version control.
- `create_gitignore.sh`: Script to create or update the `.gitignore` file.

## Known Limitations
- The model is trained on synthetic data and may not generalize well to real-world data.
- The dataset structure must be consistent; otherwise, the application may fail to process the data correctly.
- The current implementation does not handle missing or incomplete data gracefully.
- The feasibility score calculation uses fixed weights, which may not be optimal for all scenarios.

## Proposed Backlog
- **Data Validation**: Implement data validation to handle missing or incomplete data.
- **Model Improvement**: Train the model on real-world data to improve its accuracy and generalization.
- **Dynamic Weights**: Allow dynamic adjustment of weights for feasibility score calculation.
- **User Interface**: Develop a user-friendly interface for interacting with the application.
- **Deployment**: Deploy the application to a cloud platform for wider accessibility.
- **Documentation**: Improve documentation with detailed usage examples and API documentation.
