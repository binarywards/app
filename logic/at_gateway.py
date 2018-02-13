class utilities:
    http_get = "GET"
    http_post = "POST"
    http_put = "PUT"
    http_delete = "DELETE"

    def py_jax(self, url, method="GET", data_type="json", headers=None, **params):
        import requests
        if headers is None:
            headers = {}
        if method == "POST":
            request = requests.post(url=url, data=params, headers=headers)
        elif method == "PUT":
            request = requests.put(url=url, data=params, headers=headers)
        elif method == "DELETE":
            request = requests.delete(url=url, **params, headers=headers)
        else:
            request = requests.get(url=url, params=params, headers=headers)
        if data_type == "json":
            response = request.json()
        else:
            response = request.text
        return response


class urls:
    send_message = "http://api.africastalking.com/version1/messaging"
    send_airtime = "http://api.africastalking.com/version1/airtime/send"
    payment_b2c = "https://payments.africastalking.com/mobile/b2c/request"


class at_gateway:
    default_headers = {
        "accept": "application/json"
    }
    username = None
    utils = utilities()

    def __init__(self, username=None, api_key=None):
        if username is None or api_key is None:
            raise Exception('username and api_key required')
        self.default_headers["Apikey"] = api_key
        self.username = username

    def send_message(self, to, message):
        if type(to) is list:
            recipients = to[0]
            to.pop(0)
            for recipient in to:
                recipients += "," + recipient
        else:
            recipients = to
        return self.utils.py_jax(url=urls.send_message, method=utilities.http_post, headers=self.default_headers,
                                 username=self.username, to=recipients, message=message)

    def ussd_response(self, cont=False, message="Bye..."):
        if cont:
            message = "CON " + message
        else:
            message = "END " + message
        return message

    def buy_airtime_single(self, phoneNumber, amount):
        #convert recipients to JSON
        import json
        recipients = [{"phoneNumber": phoneNumber, "amount": "KES "+str(amount)}]
        recipients = json.dumps(recipients, indent=4, separators=(',', ': '))
        return self.utils.py_jax(url=urls.send_airtime, method=utilities.http_post, headers=self.default_headers,
                                 username=self.username, recipients=recipients)

    def buy_airtime(self, recipients=[{"phoneNumber": "0728824727", "amount": "KES 20"}]):
        #convert recipients to JSON
        import json
        recipients = json.dumps(recipients, indent=4, separators=(',', ': '))
        return self.utils.py_jax(url=urls.send_airtime, method=utilities.http_post, headers=self.default_headers,
                                 username=self.username, recipients=recipients)

    def send_cash_single_mpesa_b2c(self, name, phone, amount):
        headers = self.default_headers
        headers["Content-Type"] = "application/json"
        # will have to finish this later
