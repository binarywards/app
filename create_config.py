import os
import json
import traceback
try:
    data = json.dumps({
        "type": "service_account",
        "project_id": "binarywards",
        "private_key_id": os.environ.get('private_key_id', "this will fail"),
        "private_key": os.environ.get('private_key', "this will fail").replace('\\n','\n'),
        "client_email": os.environ.get('client_email', "this will fail"),
        "client_id": os.environ.get('client_id', "this will fail"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ.get('cert_url', "this will fail")
    }, indent=4, separators=(',', ': '))
    file = open(os.path.dirname(os.path.realpath(__file__))+"/binarywards-59e2153bd029.json", "w+")
    file.write(data+"\n")
    file.close()
except Exception:
    print(traceback.format_exc())