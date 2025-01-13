# app.py
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense  # type: ignore
import numpy as np
from web3 import Web3  # Import Web3
from fund_in_a_box import setup_fund  # Import the new module

# Initialize the application
def main():
    print("Starting Capetain-Cetriva application...")
    print("Setting up Hybrid Fund...")
    setup_fund()  # Call the function to set up the Hybrid Fund

if __name__ == "__main__":
    main()
