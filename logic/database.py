"""
The database will be used to store user's details
Including: phone_number, password, email and user_name
Companies: email, phone_number, password, name, company_code
Campaigns: company_code, campaign_name, details, campaign_code, custom_message
Campaigns_data: campaign_id, item_id, prize_type, prize_amount, winner, delivered, delivery_id
Ussd_sessions: session_id, phone_number, text, time_stamp
"""

import pyrebase
import os
import logic.utilities as utils

config = {
    "apiKey": os.environ.get('firebase_key', 'lost it?'),
    "authDomain": "binarywards.firebaseapp.com",
    "databaseURL": "https://binarywards.firebaseio.com",
    "storageBucket": "binarywards.appspot.com",
    "serviceAccount": os.path.dirname(os.path.realpath(__file__))+"/../binarywards-59e2153bd029.json"
}


firebase = pyrebase.initialize_app(config)

db = firebase.database()


# create user
def create_user(phone, password, fullname, email):
    password = utils.sha256(password)
    if utils.validate_phone(phone):
        phone = "254" + phone[(len(phone) - 9):len(phone)]
        db.child("app").child("users").child(phone).child("details").set(dict(password=password, name=fullname, email=email))
        return True
    else:
        return False


# email, phone_number, password, name, company_code
def create_company(email, phone_number, password, name, company_code):
    password = utils.sha256(password)
    db.child("app").child("companies").child(company_code).child("details").set(dict(
        email=email, password=password, name=name, phone=phone_number, balance=0
    ))


# company_code, campaign_name, details, campaign_code, token_type['refer', 'stored'], custom_message,
# token_type, callback, token_call, token_type
def create_campaign(company_code, campaign_name, campaign_code, message, custom_message, details,
                    callback, token_call, token_type=''):
    db.child("app").child("companies").child(company_code).child("campaigns").child(campaign_code).set(dict(
        name=campaign_name, message=message, custom_message=custom_message, details=details
    ))
    db.child("app").child("campaigns").child(campaign_code).set(dict(
        company=company_code, token_type=token_type, token_call=token_call, callback=callback
    ))


# prize_type, prize_amount, winner, delivered, delivery_id
def add_campaign_data(company_code, campaign_code, redemption_code, prize_type, prize_amount, winner):
    db.child("app").child("companies").child(company_code).child("campaigns"). \
        child(campaign_code).child("tokens").child(redemption_code).set(dict(
            prize_type=prize_type, prize_amount=prize_amount, redeemed=False
        ))


def record_reward(company_code, campaign_code, delivered, delivery_id, winner, redemption_code, prize_type, amount):
    db.child('app').child('companies').child(company_code).child('campaigns').\
        child(campaign_code).child('tokens').child(redemption_code).update(dict(
            winner=winner, delivered=delivered, delivery_id=delivery_id, redeemed=True, time=utils.human_date()
        ))
    db.child('app').child('users').child(winner).child('rewards').push(dict(
        company=company_code, campaign=campaign_code, delivery_id=delivery_id, delivered=delivered,
        code=redemption_code, time=utils.human_date(), prize_type=prize_type, amount=amount
    ))
