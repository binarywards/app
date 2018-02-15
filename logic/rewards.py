import logic.database as database
import logic.utilities as utils
from logic.at_gateway import at_gateway
import os
import traceback


class rewards:
    db = None
    gateway = None

    def __init__(self):
        self.db = database.db
        self.gateway = at_gateway(username=os.environ.get('at_user'), api_key=os.environ.get('at_key'))

    def redeem(self, redemptionCode, phoneNumber):
        message = "An error occurred"
        success = False
        status = utils.status_code.system_error
        try:
            if utils.validate_phone(phoneNumber):
                phoneNumber = "+254" + phoneNumber[(len(phoneNumber) - 9):len(phoneNumber)]
                inputs = str(redemptionCode).split(" ")
                if len(inputs) == 2:
                    campaign_code = inputs[0]
                    redemptionCode = inputs[1]
                    campaign = self.db.child('app').child("campaigns").child(campaign_code).get().val()
                    if campaign is not None:
                        company = campaign['company']
                        # Read token from db (It might not be there)
                        token = self.db.child('app').child('companies').child(company). \
                            child('campaigns').child(campaign_code).child('tokens').child(redemptionCode).get().val()
                        if token is not None:
                            campaign["token_type"] = 'stored'
                        else:
                            campaign["token_type"] = 'refer'
                        # set whether to continue rewarding the token
                        cont = False
                        # Check the type of token:
                        if campaign["token_type"] == 'stored':
                            # Check if token exists
                            if token is not None:
                                # Allow token to continue to redemption if not redeemed
                                if not token['redeemed']:
                                    cont = True
                                else:
                                    status = utils.status_code.forbidden
                                    message = "This token has already been redeemed"
                            else:
                                status = utils.status_code.not_found
                                message = "token was not found under campaign " + str(campaign_code)
                        elif campaign["token_type"] == 'refer':
                            token_call = campaign['token_call']
                            if token_call is not None and str(token_call).strip() is not "":
                                result = utils.py_jax(token_call, 'POST',
                                                      campaign_code=campaign_code, company_code=company,
                                                      token=redemptionCode, phone=phoneNumber)
                                if result["success"] or str(result["success"]).lower() is "true":
                                    token = result["token"]
                                    token['redeemed'] = False
                                    if all(key in token for key in ['redemption_code', 'prize_type', 'prize_amount']):
                                        self.db.child('app').child('companies').child(company).child('campaigns').\
                                            child(campaign_code).child('tokens').child(redemptionCode).set(token)
                                        cont = True
                                    else:
                                        status = utils.status_code.invalid_data
                                        message = str(company) + "Provided invalid prize parameters"
                                else:
                                    status = utils.status_code.invalid_data
                                    message = "Shit!"
                        else:
                            status = utils.status_code.not_implemented
                            message = "Unknown type of campaign provided"
                        if cont:
                            if token['prize_type'] == 'Airtime':
                                # Send airtime
                                result = self.gateway.buy_airtime_single(phoneNumber, token['prize_amount'])

                                if str(result["responses"][0]["status"]).lower() == 'sent':
                                    request_id = result["responses"][0]["requestId"]
                                    database.record_reward(company, campaign_code, True, request_id, phoneNumber,
                                                           redemptionCode, 'Airtime', token['prize_amount'])
                                    success = True
                                    status = utils.status_code.success
                                    message = "You have successfully redeemed KES " + str(token['prize_amount']) +\
                                              "worth of airtime to" + str(phoneNumber)
                                else:
                                    utils.async_logger("Airtime error:", result["responses"][0]["errorMessage"])
                                    message = "Unable to send airtime, please retry"
                            else:
                                database.record_reward(company, campaign_code, False, None, phoneNumber,
                                                       redemptionCode, token['prize_type'], token['prize_amount'])
                                success = True
                                status = utils.status_code.success
                                message = "You have received a custom reward, " + company + \
                                          "will be in contact to organize how you will get your reward"
                                # Send the custom sms
                                custom = self.db.child('app').child('companies').child(company). \
                                    child('campaigns').child(campaign_code).get().val()["custom_message"]
                                utils.run_in_background(at_gateway.send_message, to=phoneNumber, message=custom)
                    else:
                        status = utils.status_code.invalid_data
                        message = "Please check your code and try again"
                else:
                    status = utils.status_code.invalid_data
                    message = "Invalid input, use the format 'CAMPAIGN code'"
            else:
                status = utils.status_code.invalid_data
                message = "Invalid phone number. Phone number must be in format: +2547 XXX XXX XXX"
        except Exception as error:
            utils.async_logger(str(error), traceback.format_exc())
        return utils.api_return(success, message, status)

    def reward(self, company_code, token, campaign_code, phone):
        # 'redemption_code', 'prize_type', 'prize_amount'
        token_items = self.db.child('app').child('custom_codes').get().val()
        if token_items is not None:
            token_items = token_items[str(token)]
            return dict(success=True, token=dict(redemption_code=token,
                        prize_type=token_items['prize_type'], prize_amount=token_items['prize_amount'])), 200
        else:
            return dict(success=False, errorMessage="Token is not available"), 400
