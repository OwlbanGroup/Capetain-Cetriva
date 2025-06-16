import os
import logging

from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api import plaid_api

def create_link_token(self, user_id):
    """
    Create a link token for the client to initialize Plaid Link.
    Args:
        user_id (str): Unique identifier for the user.
    Returns:
        dict: Link token response.
    """
    try:
        response = self.client.LinkToken.create(
            {
                "user": {"client_user_id": user_id},
                "client_name": "Capetain Cetriva",
                "products": ["auth", "transactions"],
                "country_codes": ["US"],
                "language": "en",
            }
        )
        logger.info(f"Created link token for user {user_id}")
        return response
    except PlaidError as e:
        logger.error(f"Plaid error creating link token: {e}")
        return None

def exchange_public_token(self, public_token):
    """
    Exchange a public token for an access token.
    Args:
        public_token (str): The public token from Plaid Link.
    Returns:
        dict: Access token response.
    """
    try:
        response = self.client.Item.public_token.exchange(public_token)
        logger.info("Exchanged public token for access token")
        return response
    except PlaidError as e:
        logger.error(f"Plaid error exchanging public token: {e}")
        return None

def get_accounts(self, access_token):
    """
    Retrieve accounts linked to the access token.
    Args:
        access_token (str): The access token.
    Returns:
        dict: Accounts information.
    """
    try:
        response = self.client.Auth.get(access_token)
        logger.info("Retrieved accounts information")
        return response
    except PlaidError as e:
        logger.error(f"Plaid error retrieving accounts: {e}")
        return None
