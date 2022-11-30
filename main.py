from datetime import datetime
import models
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_mail import Mail


app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

url_prefix = "/api/v1/usermng/"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'raj.imdeveloper@gmail.com'
app.config['MAIL_PASSWORD'] = 'cybevhpgqmxozhpx'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'raj.imdeveloper@gmail.com'

mail = Mail(app)


def _corsify_actual_response(response):
    # response.headers.add("Access-Control-Allow-Origin", "*")
    response.status_code = 200
    return response


@app.route(f'{url_prefix}/signup', methods=["POST", "OPTIONS"])
def index():
    try:
        data = request.json
        if request.method == "OPTIONS":
            return _corsify_actual_response(jsonify({"status": None}))
        elif data == None:
            return _corsify_actual_response(jsonify({"status": False, "message": "No data provided"}))

        email = data['email']
        password = data['password']
        username = data["username"]
        mobile_no = data["mobile_no"]

        status, message, data = models.insert_user(
            username, email, password, mobile_no)
        return jsonify({"Data": data, "Status": status, "Message": message})
    except Exception as e:
        return jsonify({"Status": False, "Message": str(e)})


@app.route(f'{url_prefix}/signin', methods=["POST", "OPTIONS"])
def login():
    try:
        data = request.json
        if request.method == "OPTIONS":
            return _corsify_actual_response(jsonify({"status": None}))
        elif data == None:
            return _corsify_actual_response(jsonify({"status": False, "message": "No data provided"}))

        email = data['email']
        password = data['password']

        status, message, data = models.login(email, password)
        return jsonify({"Data": data, "Status": status, "Message": message})
    except Exception as e:
        return jsonify({"Status": False, "Message": str(e)})


@app.route(f'{url_prefix}/forgetPassword', methods=["OPTIONS", "POST"])
def forgetPassword():
    try:
        data = request.json
        if request.method == "OPTIONS":
            return _corsify_actual_response(jsonify({"status": None}))
        elif data == None:
            return _corsify_actual_response(jsonify({"status": False, "message": "No data provided"}))
        email = data['email']
        username = data['username']
        status, message = models.forget_password(email, username)
        return jsonify({"Status": status, "Message": message})
    except Exception as e:
        return jsonify({"Status": False, "Message": str(e)})


@app.route(f'{url_prefix}/resetPassword', methods=["OPTIONS", "POST"])
def resetPassword():
    try:
        data = request.json
        if request.method == "OPTIONS":
            return _corsify_actual_response(jsonify({"status": None}))
        elif data == None:
            return _corsify_actual_response(jsonify({"status": False, "message": "No data provided"}))
        email = data['email']
        password = data['password']
        new_password = data['new_password']
        status, message = models.reset_password(email, password, new_password)
        return jsonify({"Status": status, "Message": message})
    except Exception as e:
        return jsonify({"Status": False, "Message": str(e)})


if __name__ == '__main__':
    app.run(debug=True)
