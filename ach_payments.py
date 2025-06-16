import logging
import requests
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ACHPayments:
    def __init__(self):
        # Initialize ACH payment gateway credentials/configuration here
        self.api_url = "https://api.example-ach-gateway.com/payments"
        self.api_key = "your_api_key_here"
        self.max_retries = 3
        self.retry_delay = 2  # seconds

    def create_payment(
        self,
        account_number,
        routing_number,
        amount,
        description="",
    ):
        """
        Create an ACH payment request.
        Args:
            account_number (str): Bank account number to debit/credit.
            routing_number (str): Bank routing number.
            amount (float): Amount to transfer.
            description (str): Optional description for the payment.
        Returns:
            dict: Payment response or status.
        """
        payload = {
            "account_number": account_number,
            "routing_number": routing_number,
            "amount": amount,
            "description": description,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(
                    f"Attempt {attempt}: Creating ACH payment of {amount} to account "
                    f"{account_number} with routing {routing_number}"
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

    def get_payment_status(self, transaction_id):
        """
        Retrieve the status of an ACH payment by transaction ID.
        Args:
            transaction_id (str): The transaction identifier.
        Returns:
            dict: Payment status information.
        """
        status_url = f"{self.api_url}/{transaction_id}/status"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        try:
            logger.info(f"Retrieving status for transaction {transaction_id}")
            response = requests.get(
                status_url, headers=headers, timeout=10
            )
            response.raise_for_status()
            status_response = response.json()
            logger.info(f"Payment status retrieved: {status_response}")
            return status_response
        except requests.RequestException as e:
            logger.error(f"Error retrieving payment status: {e}")
            return {"status": "failure", "error": str(e)}
