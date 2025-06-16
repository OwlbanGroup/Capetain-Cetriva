import requests
import logging
import json
import os
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


CACHE_FILE = "routing_number_cache.json"
CACHE_TTL = 86400  # 24 hours in seconds


def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                cache = json.load(f)
            # Remove expired cache entries
            current_time = time.time()
            cache = {k: v for k, v in cache.items() if current_time - v["timestamp"] < CACHE_TTL}
            return cache
        except Exception as e:
            logger.error(f"Failed to load cache: {e}")
            return {}
    return {}


def save_cache(cache):
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f)
    except Exception as e:
        logger.error(f"Failed to save cache: {e}")


def get_routing_number(bank_name):
    """
    Get the official routing number for a given bank name.
    Uses a cached local store to reduce API calls.
    Args:
        bank_name (str): Name of the bank.
    Returns:
        str: Routing number or error message.
    """
    cache = load_cache()
    bank_name_lower = bank_name.lower()
    if bank_name_lower in cache:
        logger.info(f"Cache hit for bank: {bank_name}")
        return cache[bank_name_lower]["routing_number"]

    # Example API endpoint (not real, for demonstration only)
    api_url = f"https://www.frbservices.org/EPaymentsDirectory/search?searchString={bank_name.replace(' ', '%20')}&searchType=NAME"
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code != 200:
            error_msg = f"Failed to retrieve data from the Federal Reserve API. Status code: {response.status_code}"
            logger.error(error_msg)
            return error_msg
        # The actual parsing logic depends on the API response format (likely XML or JSON)
        # For demonstration, assume JSON response with routingNumber field
        try:
            data = response.json()
            routing_number = data.get("routingNumber", None)
            if routing_number:
                cache[bank_name_lower] = {"routing_number": routing_number, "timestamp": time.time()}
                save_cache(cache)
                return routing_number
            else:
                error_msg = "Routing number not found in API response."
                logger.error(error_msg)
                return error_msg
        except json.JSONDecodeError:
            error_msg = "Failed to parse API response as JSON."
            logger.error(error_msg)
            return error_msg
    except requests.RequestException as e:
        error_msg = f"An error occurred during API request: {str(e)}"
        logger.error(error_msg)
        return error_msg


if __name__ == "__main__":
    bank_name = "Capetain Cetriva"
    result = get_routing_number(bank_name)
    print(f"Routing number search result for '{bank_name}': {result}")
