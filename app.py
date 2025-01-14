import logging
from flask import Flask, render_template, request
import numpy as np
from fund_in_a_box import setup_fund
from model_setup import model, train_model

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

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
        # Load historical investment data and labels (placeholder)
        historical_data = np.array([[0.5, 0.3, 0.2], [0.6, 0.2, 0.2]])
        labels = np.array([[1, 0, 0], [0, 1, 0]])

        # Train the model on historical data
        logger.info("Training model...")
        train_model(historical_data, labels)

        # Set up the Hybrid Fund
        logger.info("Setting up fund...")
        setup_fund()
        
        logger.info("Fund setup completed successfully")
        return "Hybrid Fund setup completed!"
    except Exception as e:
        logger.error(f"Error during fund setup: {str(e)}")
        return "An error occurred during fund setup. Please try again later.", 500

@app.route('/mint_nft', methods=['POST'])
def mint_nft():
    """Handle the NFT minting request."""
    try:
        # Placeholder logic for minting an NFT
        nft_value = 250000
        logger.info(f"Minting NFT with value: ${nft_value}")
        return f"NFT minted successfully with a preset value of ${nft_value}!"
    except Exception as e:
        logger.error(f"Error during NFT minting: {str(e)}")
        return "An error occurred during NFT minting. Please try again later.", 500

if __name__ == "__main__":
    logger.info("Starting application...")
    app.run(host='0.0.0.0', port=5000, debug=True)
