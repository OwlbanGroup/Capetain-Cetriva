# Capetain-Cetriva

## Project Overview

Capetain-Cetriva is a project designed to facilitate fund management and NFT minting using advanced algorithms and API integrations. The project leverages the Deepseek, Singularity, and Intellasense APIs to enhance asset allocation strategies.

## Installation Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/Capetain-Cetriva.git
   cd Capetain-Cetriva
   ```

2. Set up a virtual environment:

   ```bash
   python3 -m venv new_venv
   source new_venv/bin/activate  # On Windows use `new_venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Replace the Infura project ID in `app.py` and `fund_in_a_box.py` with your actual project ID.

## API Integration

The project integrates the following APIs:

- **Deepseek API**: Used for historical data analysis.
- **Singularity API**: Provides predictive modeling based on insights from Deepseek.
- **Intellasense API**: Refines predictions to align with current market trends.

## Usage Instructions

### Setup Fund

To set up a fund, send a POST request to the `/setup_fund` endpoint with the following JSON body:

```json
{
  "initial_allocations": {
    "equities": 0.5,
    "bonds": 0.3,
    "real_estate": 0.2
  }
}
```

**Expected Response**:

```json
{
  "message": "Hybrid Fund setup completed!",
  "result": {
    "equities": 0.45,
    "bonds": 0.35,
    "real_estate": 0.2
  }
}
```

### Mint NFT

To mint an NFT, send a POST request to the `/mint_nft` endpoint. No body is required.

**Expected Response**:

```json
{
  "message": "NFT minted successfully! ID: <nft_id>, Value: $250000"
}
```

## Error Handling

Common errors include:

- **Ethereum Connection Error**: Ensure your Infura project ID is valid and that you have an internet connection.
- **API Call Failures**: Check the API documentation for the respective services for troubleshooting.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.
