from flask import Flask, render_template, request
import numpy as np
from fund_in_a_box import setup_fund  # Import the new module
from model_setup import model, train_model  # Import the model and training function

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setup_fund', methods=['POST'])
def setup_fund_route():
    # Load historical investment data and labels (placeholder)
    historical_data = np.array([[0.5, 0.3, 0.2], [0.6, 0.2, 0.2]])  # Example data
    labels = np.array([[1, 0, 0], [0, 1, 0]])  # Example labels for training

    # Train the model on historical data
    train_model(historical_data, labels)

    # Set up the Hybrid Fund
    setup_fund()  # Call the function to set up the Hybrid Fund
    return "Hybrid Fund setup completed!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
