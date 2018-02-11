import create_config
from flask import Flask, redirect, request, Response, url_for, send_from_directory
from flask_socketio import SocketIO, send, emit
import json
import os
import traceback
from logic.utilities import status_code
import logic.utilities as utils
import logic.router as router


data_sent = None

app = Flask(__name__, static_folder='docs', template_folder='docs')
app.config['SECRET_KEY'] = utils.random_string(16)
socketio = SocketIO(app)
red_actions = router.actions()
help_actions = {}
for key in red_actions.keys():
    action = red_actions[key]
    action.pop("function")
    help_actions[key] = action


def dict_to_json(dct):
    return json.dumps(dct, indent=4, separators=(',', ': '))


def handle_parameters(params, headers):
    arguments = {}
    success = True
    for param in params:
        arguments[param] = data_sent.get(param, None)
        if arguments[param] is None:
            success = False
            return success, arguments
    for param in headers:
        try:
            arguments[param] = request.headers[param]
        except KeyError:
            success = False
            return success, arguments
    return success, arguments


def handle_dict_par(params, data):
    arguments = {}
    success = True
    for param in params:
        try:
            arguments[param] = data[param]
        except KeyError:
            success = False
            return success, arguments
    return success, arguments


@app.before_request
def before_request():
    if request.url.startswith('http://') and (not request.url.startswith('http://localhost')):
        url = request.url.replace('http://', 'https://', 1)
        return redirect(location=url, code=status_code.redirect)
    global data_sent
    if request.headers.get('Content-Type') == "application/json":
        print("Using form")
        data_sent = request.json
    else:
        print("Using form")
        data_sent = request.form
        print(data_sent)


@app.route('/')
@app.route('/index.php')
@app.route('/default.aspx')
def index():
    return app.send_static_file('index.html')


@app.route('/logo')
def logo():
    return send_from_directory(app.static_folder, 'img/royals.png')


# serve files from root url instead of static directory
@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


@app.route('/api', methods=["POST", "GET"])
def api_main():
    out = {
        "success": True,
        "message": "This is a help command. Read the key actions to see all the available actions on the api",
        "actions": help_actions
    }
    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/api/<string:api_action>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_actions(api_action):
    status = status_code.system_error
    out = {
        "success": False,
        "message": "Use POST for action "+api_action+" and provide all the parameters as in the key params and headers."
    }
    actions = router.actions()
    try:
        if api_action in actions:
            params = actions[api_action]["parameters"]
            headers = actions[api_action]["headers"]
            description = actions[api_action]["description"]
            method = actions[api_action]["method"]
            out["params"] = params
            out["headers"] = headers
            out["message"] = description
            out["method"] = method
            if request.method == method:
                success, args = handle_parameters(params, headers)
                if success:
                    if "function" in actions[api_action]:
                        out, status = actions[api_action]["function"](**args)
                    else:
                        status = status_code.not_implemented
                        out["message"] = "Action "+api_action+" is not yet implemented, come back soon"
                else:
                    status = status_code.invalid_data
                    out["message"] = "Please provide all the headers and parameters as " \
                                     "provided in key headers and params"
            else:
                status = status_code.method_not_allowed
                out["message"] = "Wrong method, please retry using method "+method
        else:
            status = status_code.not_found
            out["message"] = "Unknown action, please check: "+url_for("/api")
    except Exception:
        utils.async_logger("API action error:", traceback.format_exc(4))
        out["message"] = "An error occurred"
    return Response(dict_to_json(out), content_type="text/json"), status


@socketio.on('connect', namespace='/realtime')
def connected():
    print("Client connected")
    send({'success': False})


@socketio.on('disconnect', namespace='/realtime')
def disconnected():
    print("Client Disconnected")
    send({'success': False})


@socketio.on('message')
def plain_message(message):
    print(message)


# Handle JSON data from an unnamed event
@socketio.on('json', namespace='/realtime')
def handle_json(data):
    emit("json", {
        'action': 'acknowledge',
        'success': True
    })
    api_action = data['action']
    status = status_code.system_error
    out = {
        "success": False,
        "message": "Use POST for action " + api_action + " and provide all the parameters as in the key params and headers."
    }
    try:
        actions = router.actions()
        if api_action in actions:
            params = actions[api_action]["parameters"]
            headers = actions[api_action]["headers"]
            description = actions[api_action]["description"]
            out["params"] = params
            out["headers"] = headers
            out["message"] = description
            success, args = handle_dict_par(params+headers, data)
            if success:
                if "function" in actions[action]:
                    out, status = actions[action]["function"](**args)
                else:
                    status = status_code.not_implemented
                    out["message"] = "Action "+api_action+" is not yet implemented, come back soon"
            else:
                status = status_code.invalid_data
                print(params + headers)
                out["message"] = "Please provide all the headers and parameters as " \
                                 "provided in key headers and params"
        else:
            status = status_code.not_found
            out["message"] = "Unknown action, please check: "+url_for("/api")
    except Exception:
        utils.async_logger("API action error:", traceback.format_exc())
        out["message"] = "An error occurred"
    out['action'] = action
    out['status'] = status
    emit('json', out)


@socketio.on_error(namespace='/realtime')
def handle_soc_err(error):
    print('An error occurred')
    print(error)


@socketio.on_error_default
def socket_error(e):
    print('universal error')
    print(e)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app=app, host='0.0.0.0', port=port)
