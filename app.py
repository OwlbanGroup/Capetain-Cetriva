import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense  # type: ignore
import numpy as np
from web3 import Web3  # Import Web3

# Initialize Web3 connection (replace with your Infura or local node URL)
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))

# Check if connected to Ethereum
if w3.isConnected():
    print("Connected to Ethereum network")
else:
    print("Failed to connect to Ethereum network")

# Define a simple model
model = Sequential([
    Dense(10, activation='relu', input_shape=(3,)),
    Dense(10, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Dummy data
X = np.array([[0, 1, 2], [1, 2, 3], [2, 3, 4]])
y = np.array([0, 1, 0])

# Train the model
model.fit(X, y, epochs=10)

# Make predictions
predictions = model.predict(X)

# Format and print predictions
for i, prediction in enumerate(predictions):
    print(f"Prediction for input {X[i]}: {prediction[0]}")
