"""ACH payment gateway integration with retry logic and status tracking."""

import logging
import os
import time
from typing import Any, Dict, Optional

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ACHPayments:
    """Client for an ACH payment gateway supporting create and status queries."""
    def __init__(self) -> None:
        # Initialize ACH payment gateway credentials/configuration here
        self.api_url: str = "https://api.example-ach-gateway.com/payments"
        self.api_key: Optional[str] = os.getenv("ACH_API_KEY")
        if not self.api_key:
            logger.warning("ACH_API_KEY environment variable is not set.")
        self.max_retries: int = 3
        self.retry_delay: int = 2  # seconds

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

        payload: Dict[str, Any] = {
            "account_number": account_number,
            "routing_number": routing_number,
            "amount": amount,
            "description": description,
        }
        headers: Dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
            "Content-Type": "application/json",
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(
                    "Attempt %s: Creating ACH payment of %s to account "
                    "%s with routing %s",
                    attempt, amount, account_number, routing_number,
                )
                response = requests.post(self.api_url, json=payload, headers=headers, timeout=10)
                response.raise_for_status()
                payment_response: Dict[str, Any] = response.json()
                logger.info("ACH payment created successfully: %s", payment_response)
                return payment_response
            except requests.RequestException as e:
                logger.error("Error creating ACH payment on attempt %s: %s", attempt, e)
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
                else:
                    return {"status": "failure", "error": str(e)}
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.error(
                    "Unexpected error creating ACH payment on attempt %s: %s", attempt, e
                )
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
                else:
                    return {"status": "failure", "error": str(e)}
        return {"status": "failure", "error": "All attempts failed"}

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

        status_url: str = f"{self.api_url}/{transaction_id}/status"
        headers: Dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
        }
        try:
            logger.info("Retrieving status for transaction %s", transaction_id)
            response = requests.get(
                status_url, headers=headers, timeout=10
            )
            response.raise_for_status()
            status_response: Dict[str, Any] = response.json()
            logger.info("Payment status retrieved: %s", status_response)
            return status_response
        except requests.RequestException as e:
            logger.error("Error retrieving payment status: %s", e)
            return {"status": "failure", "error": str(e)}
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Unexpected error retrieving payment status: %s", e)
            return {"status": "failure", "error": str(e)}
