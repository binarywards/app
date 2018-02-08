class stitcher:
    """
    Fot this service the ussd is necessary to receive codes from customers
    We therefore request a redemption code in the first step.
    We end there by a confirmation of the redemption or we can move forward to ask the user to register and
    earn points instead of instant rewards.
    These rewards can later be redeemed to cash, airtime, shopping vouchers among other things
    """
    def handle_ussd(self, sessionid, phoneNumber, serviceCode, text):
        all_params = text.split("*")
        if self.session_exists(sessionid):
            message = ""
        else:
            self.start_session(sessionid, phoneNumber)

    def start_session(self, sessionid, phoneNumber):
        pass

    def session_exists(self, sessionid):
        pass
