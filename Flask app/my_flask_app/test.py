import unittest
import json
from my_flask_app.app import app
import os

class FlaskAPITestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        print("Running test_home: Testing the home route for API status.")
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'EV Charging Investment API is running', response.data)

    def test_train(self):
        print("Running test_train: Testing the train endpoint with valid data.")
        data = [
            {"cost": 0.5, "demand": 0.7, "regulatory": 0.3, "target": 1.0},
            {"cost": 0.6, "demand": 0.8, "regulatory": 0.4, "target": 1.2}
        ]
        response = self.app.post('/train', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Model trained and saved successfully', response.data)

    def test_predict(self):
        print("Running test_predict: Testing the predict endpoint with valid data.")
        # Ensure model is trained first
        self.test_train()

        # Test the predict endpoint with valid data
        data = [
            {"cost": 0.5, "demand": 0.7, "regulatory": 0.3},
            {"cost": 0.6, "demand": 0.8, "regulatory": 0.4}
        ]
        response = self.app.post('/predict', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'prediction', response.data)

if __name__ == '__main__':
    unittest.main() 