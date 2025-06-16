import logging
import os
import requests
import time
from typing import Optional, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ACHPayments:
    def __init__(self):
        # Initialize ACH payment gateway credentials/configuration here
        self.api_url = "https://api.example-ach-gateway.com/payments"
        self.api_key = os.getenv("ACH_API_KEY")
        if not self.api_key:
            logger.warning("ACH_API_KEY environment variable is not set.")
        self.max_retries = 3
        self.retry_delay = 2  # seconds

    def create_payment(
        self,
        account_number: str,
        routing_number: str,
        amount: float,
        description: str = "",
    ) -> Optional[Dict[str, Any]]:
        """
        Create an ACH payment request.
        Args:
            account_number (str): Bank account number to debit/credit.
            routing_number (str): Bank routing number.
            amount (float): Amount to transfer.
            description (str): Optional description for the payment.
        Returns:
            dict or None: Payment response or None if failure.
        """
        if amount <= 0:
            logger.error("Amount must be greater than zero.")
            return None
        if not account_number or not routing_number:
            logger.error("Account number and routing number must be provided.")
            return None

        payload = {
            "account_number": account_number,
            "routing_number": routing_number,
            "amount": amount,
            "description": description,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
            "Content-Type": "application/json",
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(
                    f"Attempt {attempt}: Creating ACH payment of {amount} to account "
                    f"{account_number} with routing "
                    f"{routing_number}"
                )
                response = requests.post(self.api_url, json=payload, headers=headers, timeout=10)
                response.raise_for_status()
                payment_response = response.json()
                logger.info(f"ACH payment created successfully: {payment_response}")
                return payment_response
            except requests.RequestException as e:
                logger.error(f"Error creating ACH payment on attempt {attempt}: {e}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
                else:
                    return {"status": "failure", "error": str(e)}

    def get_payment_status(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve the status of an ACH payment by transaction ID.
        Args:
            transaction_id (str): The transaction identifier.
        Returns:
            dict or None: Payment status information or None if failure.
        """
        if not transaction_id:
            logger.error("Transaction ID must be provided.")
            return None

        status_url = f"{self.api_url}/{transaction_id}/status"
        headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
        }
        try:
            logger.info(f"Retrieving status for transaction {transaction_id}")
            response = requests.get(
                status_url, headers=headers, timeout=10
            )
            response.raise_for_status()
            status_response = response.json()
            logger.info(
                f"Payment status retrieved: {status_response}"
            )
            return status_response
        except requests.RequestException as e:
            logger.error(f"Error retrieving payment status: {e}")
            return {"status": "failure", "error": str(e)}
