"""
Take's api routes and resolves them to the right functions with their responses
"""

from logic.users import users


def actions(socketio):
    user = users()
    return {
        "user_login": {
            "description": "",
            "method": "POST",
            "parameters": ["email", "password"],
            "headers": [],
            "function": user.login
        },
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
        }
    }

