import os
import logging
from typing import Optional, Dict, Any

from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.configuration import Configuration
from plaid.exceptions import ApiException

logger = logging.getLogger(__name__)

class PlaidIntegration:
    def __init__(self):
        configuration = Configuration(
            host="https://sandbox.plaid.com",
            api_key={
                'clientId': os.getenv('PLAID_CLIENT_ID'),
                'secret': os.getenv('PLAID_SECRET'),
            }
        )
        self.client = plaid_api.PlaidApi(configuration)
        
    def create_link_token(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Create a link token for the client to initialize Plaid Link.
        Args:
            user_id (str): Unique identifier for the user.
        Returns:
            dict or None: Link token response.
        """
        try:
            request = LinkTokenCreateRequest(
                user=LinkTokenCreateRequestUser(client_user_id=user_id),
                client_name="Capetain Cetriva",
                products=[Products.AUTH, Products.TRANSACTIONS],
                country_codes=[CountryCode.US],
                language="en"
            )
            response = self.client.link_token_create(request)
            logger.info(f"Created link token for user {user_id}")
            return response.to_dict()
        except ApiException as e:
            logger.error(f"Plaid error creating link token: {e}")
            return None

    def exchange_public_token(self, public_token: str) -> Optional[Dict[str, Any]]:
        """
        Exchange a public token for an access token.
        Args:
            public_token (str): The public token from Plaid Link.
        Returns:
            dict or None: Access token response.
        """
        try:
            response = self.client.item_public_token_exchange(public_token)
            logger.info("Exchanged public token for access token")
            return response.to_dict()
        except ApiException as e:
            logger.error(f"Plaid error exchanging public token: {e}")
            return None

    def get_accounts(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve accounts linked to the access token.
        Args:
            access_token (str): The access token.
        Returns:
            dict or None: Accounts information.
        """
        try:
            response = self.client.auth_get(access_token)
            logger.info("Retrieved accounts information")
            return response.to_dict()
        except ApiException as e:
            logger.error(f"Plaid error retrieving accounts: {e}")
            return None
