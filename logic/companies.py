import logic.database as database
import logic.utilities as utils
import traceback
import os
from logic.at_gateway import at_gateway


class company:
    db = None
    gateway = None

    def __init__(self):
        self.db = database.db
        self.gateway = at_gateway(username=os.environ.get('at_user'), api_key=os.environ.get('at_key'))

    def add_login_details(self, company_code, token):
        self.db.child('app').child('companies').child(company_code). \
            child('login_records').child(token).set(dict(time=utils.human_date(), active=True))
        self.db.child('app').child('companies').child(company_code). \
            child('login_records').child(token).child('history'). \
            push(dict(time=utils.human_date(), action='User logged in.'))

    def logged_in(self, company_code, token):
        record = self.db.child('app').child('companies').child(company_code). \
            child('login_records').child(token).get().val()
        if record is not None:
            if record["active"]:
                return True
            else:
                return False
        else:
            return False

    def update_password(self, company_code, old_password, new_password):
        status = utils.status_code.system_error
        message = "Unknown error occurred, please retry"
        success = False
        try:
            comp = self.db.child('app').child('companies').child(company_code).child('details').get().val()
            if comp is not None:
                password = utils.sha256(old_password)
                if comp['password'] == password:
                    if new_password is not None and len(new_password) >= 8:
                        self.db.child('app').child('companies').child(company_code).child('details'). \
                            update(dict(password=utils.sha256(new_password)))
                        message = "Password updated"
                        status = utils.status_code.success
                        success = True
                    else:
                        message = "Invalid password, password must be at least 8 characters"
                        status = utils.status_code.invalid_data
                else:
                    status = utils.status_code.forbidden
                    message = "Wrong password"
            else:
                message = "Company does not exist"
                status = utils.status_code.not_found
        except Exception as error:
            utils.async_logger(str(error), traceback.format_exc(4))
        return utils.api_return(success, message, status)

    def company_login(self, company_code, password):
        status = utils.status_code.system_error
        message = "Unknown error occurred, please retry"
        success = False
        try:
            comp = self.db.child('app').child('companies').child(company_code).child('details').get().val()
            if comp is not None:
                password = utils.sha256(password)
                if comp['password'] == password:
                    # Generate a token
                    import string
                    token = utils.random_string(16, string.ascii_letters + string.digits)
                    utils.run_in_background(self.add_login_details, company_code=company_code, token=token)
                    message = dict(token=token, name=comp['name'], email=comp['email'],
                                   balance=comp['balance'], phone=comp['phone'])
                    status = utils.status_code.success
                    success = True
                else:
                    status = utils.status_code.forbidden
                    message = "Wrong password"
            else:
                message = "Company does not exist"
                status = utils.status_code.not_found
        except Exception as error:
            utils.async_logger(str(error), traceback.format_exc(4))
        return utils.api_return(success, message, status)

    def register_company(self, email, phone_number, password, name, company_code):
        status = utils.status_code.system_error
        message = "Unknown error occurred, please retry"
        success = False
        try:
            if utils.validate_phone(phone_number):
                phone = "+254" + phone_number[(len(phone_number) - 9):len(phone_number)]
                if utils.validate_email(email):
                    if company_code is not None and str(company_code).isalpha() and len(company_code) <= 6:
                        existing_company = self.db.child("app").child("companies").child(company_code).get().val()
                        if existing_company is None:
                            if len(str(password)) >= 8:
                                database.create_company(email, phone, password, name, company_code)
                                custom = utils.random_string(6, "0123456789")
                                database.add_custom_token(custom, 'Airtime', '20')
                                params = dict(to=phone, message="Welcome to Bina Rywards." +
                                                                "\nUse the welcome token below to receive KES 20 airtime" +
                                                                " from our website.\nToken: BINA " + str(
                                    custom) + "\nOr " +
                                                                "visit: https://binarywards.tech/#redeem/BINA/" + str(
                                    custom) + "\n")
                                utils.run_in_background(self.gateway.send_message, **params)
                                status = utils.status_code.success
                                success = True
                                message = name + "(" + company_code + ")" + " Added successfully"
                            else:
                                message = "Invalid password, password must be at least 8 characters"
                                status = utils.status_code.invalid_data
                        else:
                            status = utils.status_code.forbidden
                            message = "Company code " + str(company_code) + " already exists"
                    else:
                        status = utils.status_code.invalid_data
                        message = "Company code can contain letters A-Z and must be less than or equal to characters"
                else:
                    status = utils.status_code.invalid_data
                    message = "Email invalid or does not exist"
            else:
                status = utils.status_code.invalid_data
                message = "Invalid phone number, use the format 2547 XXX XXX XXX"
        except Exception as e:
            utils.async_logger("Error registering company", str(e))
        return utils.api_return(success, message, status)

    def add_campaign(self, company_code, campaign_name, campaign_code, message, custom_message, details,
                     callback, token_call, token):
        status = utils.status_code.system_error
        camp_message = message
        message = "Unknown error occurred, please retry"
        success = False
        try:
            if self.logged_in(company_code, token):
                current = self.db.child('app').child('campaigns').child(campaign_code).get().val()
                if current is None:
                    if self.db.child('app').child('companies').child(company_code).get().val() is not None:
                        database.create_campaign(company_code,
                                                 campaign_name, campaign_code, camp_message, custom_message, details,
                                                 callback,
                                                 token_call)
                        message = "Campaign " + str(campaign_name) + "Added successfully"
                        success = True
                        status = utils.status_code.success
                    else:
                        status = utils.status_code.not_found
                        message = "Company does not exist"
                else:
                    status = utils.status_code.forbidden
                    message = "Campaign already exist"
            else:
                status = utils.status_code.forbidden
                message = "Invalid authentication code"
        except Exception:
            utils.async_logger("Error adding campaign", traceback.format_exc(4))
        return utils.api_return(success, message, status)

    def read_campaigns(self, company_code, token):
        success = False
        message = "Unknown error occurred"
        status = utils.status_code.system_error
        try:
            if self.logged_in(company_code, token):
                if self.db.child('app').child('companies').child(company_code).get().val() is not None:
                    campaigns = self.db.child('app').child('companies').child(company_code).child(
                        'campaigns').get().val()
                    if campaigns is None:
                        campaigns = dict()
                    message = []
                    for key in campaigns.keys():
                        message.append(dict(
                            campaign_code=key,
                            custom_message=campaigns[key]['custom_message'],
                            details=campaigns[key]['details'],
                            message=campaigns[key]['message'],
                            name=campaigns[key]['name']))
                    success = True
                    status = utils.status_code.success
                else:
                    message = "Company does not exist"
            else:
                status = utils.status_code.forbidden
                message = "Invalid authentication code"
        except Exception:
            utils.async_logger("Error reading campaigns", traceback.format_exc())
        return utils.api_return(success, message, status)

    def read_campaign(self, company_code, campaign_code, token):
        status = utils.status_code.system_error
        message = "Unknown error occurred, please retry"
        success = False
        try:
            if self.logged_in(company_code, token):
                current = self.db.child('app').child('campaigns').child(campaign_code).get().val()
                if current is not None:
                    if self.db.child('app').child('companies').child(company_code).get().val() is not None:
                        campaign = self.db.child('app').child('companies').child(company_code). \
                            child('campaigns').child(campaign_code).get().val()
                        message = dict()
                        message['name'] = campaign['name']
                        message['campaign_code'] = campaign_code
                        message['details'] = campaign['details']
                        message['message'] = campaign['message']
                        message['custom_message'] = campaign['custom_message']
                        message['callback'] = current['callback']
                        message['token_call'] = current['token_call']
                        message['total_spent'] = utils.fill_default(current, 'total_spent', 0)
                        success = True
                        status = utils.status_code.success
                    else:
                        status = utils.status_code.not_found
                        message = "Company does not exist"
                else:
                    status = utils.status_code.not_found
                    message = "Campaign not found"
            else:
                status = utils.status_code.forbidden
                message = "Invalid authentication code"
        except Exception as error:
            utils.async_logger(str(error), traceback.format_exc(4))
        return utils.api_return(success, message, status)

    def add_token(self, company_code, campaign_code, token, redeem_code, ryward_type, amount):
        success = False
        message = "Unknown error occurred"
        status = utils.status_code.system_error
        try:
            if self.logged_in(company_code, token):
                if self.db.child('app').child('companies').child(company_code).get().val() is not None:
                    code_exist = self.db.child('app').child('companies').child(company_code).\
                        child('campaigns').child(campaign_code).child('tokens').child(redeem_code).get().val()
                    if code_exist is None:
                        if str(amount).isnumeric():
                            self.db.child('app').child('companies').child(company_code).child('campaigns'). \
                                child(campaign_code).child('tokens').child(redeem_code).\
                                set(dict(redemption_code=redeem_code, prize_type=ryward_type,
                                         prize_amount=amount, redeemed=False))
                            message = "Token added successfully"
                            status = utils.status_code.success
                            success = True
                        else:
                            message = "Amount must be numeric"
                            status = utils.status_code.invalid_data
                    else:
                        status = utils.status_code.forbidden
                        message = "This code already exists"
                else:
                    status = utils.status_code.not_found
                    message = "Company not found"
            else:
                status = utils.status_code.forbidden
                message = "Invalid authentication code"
        except Exception as error:
            utils.async_logger(str(error), traceback.format_exc(4))
        return utils.api_return(success, message, status)
