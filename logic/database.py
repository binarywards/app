"""
The database will be used to store user's details
Including: phone_number, password, email and user_name
Companies: email, phone_number, password, name, use_code
Campaigns: use_code, campaign_name, details, campaign_code, custom_message
Campaigns_data: campaign_id, item_id, prize_type, prize_amount, winner, delivered, delivery_id
Ussd_sessions: session_id, phone_number, text, time_stamp
"""

import pyrebase
import os
import json

config = {
    "apiKey": "apiKey",
    "authDomain": "binarywards.firebaseapp.com",
    "databaseURL": "https://binarywards.firebaseio.com",
    "storageBucket": "binarywards.appspot.com",
    "serviceAccount": os.path.dirname(os.path.realpath(__file__))+"/../binarywards-59e2153bd029.json"
}


firebase = pyrebase.initialize_app(config)

db = firebase.database()

db.child("users")
db.child("companies")
db.child("campaigns")
db.child("ussd_sessions")


# create user
def create_user(phone, password, fullname, email):
    db.child("users").child("p" + phone).child("details").set(dict(password=password, name=fullname, email=email))


# email, phone_number, password, name, use_code
def create_company(email, phone_number, password, name, use_code):
    db.child("companies").child(use_code).child("details").set(dict(
        email=email, password=password, name=name, phone=phone_number
    ))


# use_code, campaign_name, details, campaign_code, custom_message, reward-type
def create_campaign(use_code, campaign_name, campaign_code, message, custom_message, details,
                    callback, reward_calls, reward_type=''):
    db.child("companies").child(use_code).child("campaigns").child(campaign_code).set(dict(
        name=campaign_name, message=message, custom_message=custom_message, details=details
    ))
    db.child("campaigns").child(campaign_code).set(dict(
        company=use_code, reward_type=reward_type, reward_calls=reward_calls, callback=callback
    ))


# prize_type, prize_amount, winner, delivered, delivery_id
def add_campaign_data(use_code, campaign_code, redemption_code, prize_type, prize_amount, winner, delivered,
                      delivery_id):
    db.child("companies").child(use_code).child("campaigns"). \
        child(campaign_code).child("prizes").child(redemption_code).set(dict(
            prize_type=prize_type, prize_amount=prize_amount, winner=winner,
            delivered=delivered, delivery_id=delivery_id
    ))

