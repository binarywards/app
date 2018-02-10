import logic.database as database
import logic.utilities as utils


class company:
    db = None

    def __init__(self):
        self.db = database.db

    def register_company(self, email, phone_number, password, name, company_code):
        status = utils.status_code.system_error
        message = "Unknown error occurred, please retry"
        success = False
        try:
            if utils.validate_phone(phone_number):
                phone = "+254" + phone_number[(len(phone_number) - 9):len(phone_number)]
                if utils.validate_email(email, True, True):
                    if company_code is not None and str(company_code).isalpha() and len(company_code)<=6:
                        existing_company = self.db.child("app").child("companies").child(company_code).get().val()
                        if existing_company is None:
                            database.create_company(email, phone, password, name, company_code)
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
        utils.api_return(success, message, status)

