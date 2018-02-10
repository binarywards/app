"""
Take's api routes and resolves them to the right functions with their responses
"""

from logic.users import users
from logic.rewards import rewards
from logic.companies import company


def actions():
    user = users()
    reward = rewards()
    comp = company()
    return {
        "user_add": {
            "description": "Registers a new user",
            "method": "POST",
            "parameters": ["phone", "email", "password", "username"],
            "headers": [],
            "function": user.register
        },
        "account_exists": {
            "description": "Checks if a phone number exists in the system. On success returns success as true",
            "method": "POST",
            "parameters": ["phone"],
            "headers": [],
            "function": user.user_exists
        },
        "redeem_token": {
            "description": "Redeems a specified token to the customer",
            "method": "POST",
            "parameters": ['redemptionCode', 'phoneNumber'],
            "headers": [],
            "function": reward.redeem
        },
        "company_add": {
            "description": "Registers a new organization",
            "method": "POST",
            "parameters": ['email', 'phone_number', 'password', 'name', 'company_code'],
            "headers": [],
            "function": comp.register_company
        },
        "company_new_campaign": {
            "description": "Adds a new campaign by an organization",
            "method": "POST",
            "parameters": ['company_code', 'campaign_name', 'campaign_code', 'message', 'custom_message', 'details', 'callback', 'token_call', 'token_type'],
            "headers": [],
            "function": comp.add_campaign
        }
    }

