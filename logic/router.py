"""
Take's api routes and resolves them to the right functions with their responses
"""

from logic.users import users
from logic.rewards import rewards


def actions(socketio):
    user = users()
    reward = rewards()
    return {
        "user_register": {
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
        }
    }

