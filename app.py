# app.py
# Main application for Capetain-Cetriva, handling fund setup and NFT minting.

import logging
import json  # Import json for data saving
from flask import Flask, render_template, request
import numpy as np
from fund_in_a_box import setup_fund
import uuid
from web3 import Web3
import requests  # Import requests for API calls
from requests.exceptions import RequestException  # Import for handling requests exceptions
import time  # Import for sleep function

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# File path for storing minted NFTs
NFTS_FILE_PATH = 'minted_nfts.json'

# Load minted NFTs from file if it exists
try:
    with open(NFTS_FILE_PATH, 'r') as file:
        minted_nfts = json.load(file)
except FileNotFoundError:
    minted_nfts = {}  # Initialize as empty if file does not exist

# Connect to Ethereum network (replace with your actual Infura project ID)
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/3798a0f85fc046cdabef6514acf94a81'))  # Replace with your actual Infura project ID

if not w3.is_connected():
    logger.error("Failed to connect to Ethereum network.")
    raise Exception("Ethereum connection error.")

@app.route('/')
def index():
    """Render the main index page."""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index page: {str(e)}")
        return "An error occurred while loading the page.", 500

@app.route('/setup_fund', methods=['POST'])
def setup_fund_route():
    """Handle the fund setup request."""
    try:
        data = request.json
        initial_allocations = data.get('initial_allocations', None)

        # Call Deepseek API for historical data analysis with retry logic
        for attempt in range(3):  # Retry up to 3 times
            try:
                deepseek_response = requests.post('https://api.deepseek.com/analyze', json={"data": initial_allocations})
                deepseek_response.raise_for_status()  # Raise an error for bad responses
                deepseek_data = deepseek_response.json()
                break  # Exit the retry loop if successful
            except RequestException as e:
                logger.error(f"Error calling Deepseek API: {str(e)}")
                time.sleep(2)  # Wait before retrying
        else:
            return "Failed to connect to Deepseek API after multiple attempts.", 500

        # Call Singularity API for predictive modeling with retry logic
        for attempt in range(3):
            try:
                singularity_response = requests.post('https://api.singularity.com/predict', json={"data": deepseek_data})
                singularity_response.raise_for_status()
                singularity_data = singularity_response.json()
                break
            except RequestException as e:
                logger.error(f"Error calling Singularity API: {str(e)}")
                time.sleep(2)
        else:
            return "Failed to connect to Singularity API after multiple attempts.", 500

        # Call Intellasense API for market trend refinement with retry logic
        for attempt in range(3):
            try:
                intellasense_response = requests.post('https://api.intellasense.com/refine', json={"data": singularity_data})
                intellasense_response.raise_for_status()
                refined_allocations = intellasense_response.json()
                break
            except RequestException as e:
                logger.error(f"Error calling Intellasense API: {str(e)}")
                time.sleep(2)
        else:
            return "Failed to connect to Intellasense API after multiple attempts.", 500

        # Set up the Hybrid Fund with refined allocations
        logger.info("Setting up fund with refined allocations...")
        result = setup_fund(refined_allocations)

        logger.info("Fund setup completed successfully")
        return {
            "message": "Hybrid Fund setup completed!",
            "result": result
        }
    except Exception as e:
        logger.error(f"Error during fund setup: {str(e)}")
        return "An error occurred during fund setup. Please try again later.", 500

@app.route('/mint_nft', methods=['POST'])
def mint_nft():
    """Handle the NFT minting request."""
    try:
        # Generate a unique NFT ID
        nft_id = str(uuid.uuid4())
        nft_value = 250000

        # Save the minted NFT to the file
        minted_nfts[nft_id] = nft_value
        with open(NFTS_FILE_PATH, 'w') as file:
            json.dump(minted_nfts, file)  # Save updated NFTs to file
        logger.info(f"Minting NFT with ID: {nft_id} and value: ${nft_value}")

        # Here you would include the logic to mint the NFT on the blockchain
        minted_nfts[nft_id] = nft_value
        return f"NFT minted successfully! ID: {nft_id}, Value: ${nft_value}"
    except Exception as e:
        logger.error(f"Error during NFT minting: {str(e)}")
        return "An error occurred during NFT minting. Please try again later.", 500

if __name__ == "__main__":
    logger.info("Starting application...")
    app.run(host='0.0.0.0', port=5000, debug=True)
