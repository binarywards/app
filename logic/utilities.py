import smtplib
import os
import random
import hashlib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from validate_email import validate_email
import pendulum
import traceback
import threading


class status_code:
    unauthorized = 401
    forbidden = 403
    method_not_allowed = 405
    invalid_data = 433
    not_found = 404
    bad_request = 400
    success = 200
    system_error = 500
    not_implemented = 501
    redirect = 302


def log_error(title, data):
    try:
        path = os.path.dirname(os.path.realpath(__file__))
        file = open(path + "/../logs/errors.md", "a+")
        file.write(">### "+title+"\n")
        file.write("*"+str(datetime.now())+"*\n")
        file.write("```\n"+data+"\n```\n\n")
        file.close()
        return True
    except IOError as e:
        print(str(e))
        return False


def api_return(success, message, status):
    return {
        "success": success,
        "message": message
    }, status


def sha256(text: str):
    hash_object = hashlib.sha256(text.encode())
    return hash_object.hexdigest()


def send_email(recipient: str, recipient_name: str, subject: str, template: str, template_values: dict,
               text_message="Please use a client that can read HTML email"):
    success = False
    status = 500
    try:
        if validate_email(recipient, verify=True):
            smtp = smtplib.SMTP("smtp.gmail.com", 587)  # initialize smtp class
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            message = template
            for key in list(template_values):
                message = message.replace(str(key), (template_values[key]))
            smtp.login(os.environ.get('smtp_user', "__hidden__"), os.environ.get('smtp_password', "__hidden__"))
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = 'From: Binarywards <binarywards@binarywards.com>'
            msg['To'] = recipient_name + ' <' + recipient + '>'
            plain = MIMEText(text_message, "plain")
            html = MIMEText(message, "html")
            msg.attach(plain)
            msg.attach(html)
            smtp.sendmail("deliverymashinani@gmail.com", recipient, msg.as_string())
            smtp.close()
            success = True
            message = "Your message was sent successfully."
        else:
            message = "Invalid or email does not exist"
        status = status_code.success
    except smtplib.SMTPException as e:
        message = "Error: Unable to send email: \n" + str(e)
        async_logger("SMTP Exception", traceback.format_exc())
    except (ConnectionRefusedError, ConnectionResetError, ConnectionResetError, ConnectionError) as e:
        message = "Connection error: Email not sent: \n"+str(e)
        async_logger("SMTP Exception", traceback.format_exc())
    except Exception as e:
        message = "Server Error: An error occurred: \n"+str(e)
        async_logger("SMTP Exception", traceback.format_exc())
    return {
        "success": success,
        "message": message,
        "status": status
    }


def random_string(size,
                  characters: str = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%&*()?"):
    return "".join(random.sample(characters, size))


def validate_phone(phone):
    phone = phone.replace("+", "")
    phone = phone.replace(" ", "")
    phone = phone.replace("-", "")
    if phone.isnumeric() and (
            (len(phone) == 9 and phone[0] == "7") or
            (len(phone) == 10 and phone[0:2] == "07") or
            (len(phone) == 12 and phone[0:4] == "2547")
    ) and (
            (0 <= int(phone[-8] + phone[-7]) < 40) or
            (60 <= int(phone[-8] + phone[-7]) < 100)
    ):

        return True, "+254"+phone[len(phone)-9:len(phone)]
    else:
        return False


def human_date(timestamp=datetime.now().timestamp(), date_only=False, time_ago=False, hours=0, minutes=0,
               sec=0, months=0, years=0, days=0):
    date = pendulum.from_timestamp(timestamp)
    date = date.add(years=years, months=months, weeks=0, days=days, hours=hours, minutes=minutes, seconds=sec)
    if date_only:
        return date.format('DD-MMM-YYYY', formatter='alternative')
    else:
        if time_ago:
            return date.diff_for_humans()
    return date.format('DD-MMM-YYYY HH:mm:ss', formatter='alternative')


def py_jax(url, method="GET", data_type="json", headers=None, **params):
    import requests
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


def async_jax(url, method="GET", data_type="json", headers=None, **params):
    threading.Thread(target=py_jax, kwargs=dict(url=url, method=method, data_type=data_type,
                                                headers=headers, **params))


def async_logger(title, data):
    print(data)
    threading.Thread(target=log_error, kwargs=dict(title=title, data=data)).start()


def run_in_background(method, **parameters):
    threading.Thread(target=method, kwargs=parameters).start()
