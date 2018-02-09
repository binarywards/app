import logic.database as database
import logic.utilities as utils


class users:
    db = None

    def __init__(self):
        self.db = database.db

    def register(self, phone, password, username=None, email=None):
        success = False
        message = "An error occurred"
        status = utils.status_code.system_error
        try:
            if utils.validate_phone(phone):
                phone = "254" + phone[(len(phone) - 9):len(phone)]
                user = self.db.child("app").child("users").child(phone).get()
                if user.val() is None:
                    if username is None:
                        username = ""
                    if email is None:
                        email = ""
                    database.create_user(phone, password, username, email)
                    message = "User added successfully"
                    status = utils.status_code.success
                    success = True
                else:
                    status = utils.status_code.invalid_data
                    message = "User already exist, login instead"
            else:
                status = utils.status_code.invalid_data
                message = "Invalid phone number"
        except Exception as e:
            utils.async_logger("Reg error", str(e))
        return utils.api_return(success, message, status)

    def login(self):
        pass

    def update_details(self):
        pass

    def logout(self):
        pass

    def single_auth(self):
        pass

    def user_exists(self, phone):
        success = False
        message = "An error occurred please retry."
        status = utils.status_code.system_error
        try:
            if utils.validate_phone(phone):
                phone = "254" + phone[(len(phone) - 9):len(phone)]
                user = self.db.child("app").child("users").child(phone).get()
                if user.val() is not None:
                    message = dict()
                    message["phone"] = user.val()["details"]
                    message["name"] = user.val()["name"]
                    status = utils.status_code.success
                    success = True
                else:
                    status = utils.status_code.not_found
                    message = "User not found"
            else:
                status = utils.status_code.invalid_data
                message = "Invalid phone number"
        except Exception as e:
            utils.async_logger("Reg error", str(e))
        return utils.api_return(success, message, status)
