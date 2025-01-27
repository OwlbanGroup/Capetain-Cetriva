# fund_in_a_box.py
# This module handles interactions with the "Fund in a Box" service from Repool.

import logging
import numpy as np  # Ensure this import is not commented out

# Ensure you have TensorFlow installed: pip install tensorflow
import tensorflow as tf  # Ensure this import is added
from tensorflow.keras.models import Sequential  # Ensure this import is added
from tensorflow.keras.layers import Dense  # type: ignore
from web3 import Web3  # Ensure this import is added

# Initialize Web3 connection (replace with your Infura or local node URL)
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_VALID_INFURA_PROJECT_ID'))  # Replace with your actual Infura project ID

if not w3.is_connected():
    logging.error("Failed to connect to Ethereum network.")
    raise Exception("Ethereum connection error.")
else:
    logging.info("Connected to Ethereum network")

# Example usage
model = Sequential()

# Define an enhanced model for investment predictions
model = Sequential([
    Dense(64, activation='relu', input_shape=(3,)),
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(3, activation='softmax')  # Output layer for 3 asset classes
])

# Compile the model for investment predictions
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Function to train the model on historical investment data
def train_model(historical_data, labels):
    """
    Train the model on historical investment data.
    Args:
        historical_data: Numpy array of historical investment data
        labels: Numpy array of corresponding labels
    """
    model.fit(historical_data, labels, epochs=50, batch_size=32, validation_split=0.2)

# Function to set up the Hybrid Fund
def setup_fund(initial_allocations=None):
    """
    Set up a Hybrid Fund using the "Fund in a Box" service with AI-driven asset allocation.
    Allows for dynamic asset classes and initial allocations.
    """
    try:
        logging.info("Setting up Hybrid Fund using Fund in a Box service with AI...")
        
        # Define initial asset allocations if not provided
        if initial_allocations is None:
            initial_allocations = {
                "equities": 0.5,  # 50% in equities
                "bonds": 0.3,     # 30% in bonds
                "real_estate": 0.2 # 20% in real estate
            }

        # Use the AI model to adjust asset allocations
        input_data = np.array([[initial_allocations["equities"], initial_allocations["bonds"], initial_allocations["real_estate"]]])
        predicted_allocation = model.predict(input_data)
        
        # Update asset allocations based on AI predictions
        initial_allocations["equities"] = predicted_allocation[0][0]
        initial_allocations["bonds"] = predicted_allocation[0][1]
        initial_allocations["real_estate"] = predicted_allocation[0][2]

        for asset, allocation in initial_allocations.items():
            logging.info(f"AI-adjusted allocation: {allocation * 100}% to {asset}.")
        
        return initial_allocations  # Return the updated allocations
    except Exception as e:
        logging.error(f"An error occurred while setting up the Hybrid Fund: {e}")
        return None
