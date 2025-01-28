# app.py
# Main application for Capetain-Cetriva, handling fund setup and NFT minting.

import logging
from flask import Flask, render_template, request
import numpy as np
from fund_in_a_box import setup_fund
import uuid
from web3 import Web3
import requests  # Import requests for API calls

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# In-memory storage for minted NFTs
minted_nfts = {
    "Owlban Group NFT": 250000,
}

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

        # Call Deepseek API for historical data analysis
        deepseek_response = requests.post('https://api.deepseek.com/analyze', json={"data": initial_allocations})
        deepseek_data = deepseek_response.json()

        # Call Singularity API for predictive modeling
        singularity_response = requests.post('https://api.singularity.com/predict', json={"data": deepseek_data})
        singularity_data = singularity_response.json()

        # Call Intellasense API for market trend refinement
        intellasense_response = requests.post('https://api.intellasense.com/refine', json={"data": singularity_data})
        refined_allocations = intellasense_response.json()

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

        # Placeholder logic for minting an NFT
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
