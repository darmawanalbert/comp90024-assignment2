# COMP90024 Team 1
# Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
# Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
# I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
# Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au

from flask import Flask, jsonify, request, make_response
import requests
import os
import json

import argparse
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from routes import request_api

APP = Flask(__name__)

### swagger specific ###
SWAGGER_URL = '/docs'
API_URL = '/static/swagger.yml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Group 1 COMP90024"
    }
)
APP.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

APP.register_blueprint(request_api.get_blueprint())

DB_HOST = os.environ.get('DBHOST') if os.environ.get('DBHOST') != None else "http://admin:admin@127.0.0.1:5984/"
DB_NAME = os.environ.get('DBNAME') if os.environ.get('DBNAME') != None else "testdb"

@APP.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@APP.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@APP.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@APP.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)

# @app.route("/",methods=["GET"])
# def get():
#     limit = 20
#     skip = 0
#     if(request.args.get('limit') != None):
#         limit = request.args.get('limit')
    
#     if(request.args.get('skip') != None):
#         skip = request.args.get('skip')

#     url = f"{DB_HOST}{DB_NAME}"
#     query = {"selector": {},"limit": int(limit), "skip": int(skip)}
#     headers = {'Content-Type': 'application/json'}
#     response = requests.post(f"{url}/_find",headers=headers,data=json.dumps(query))
#     response_json = json.loads(response.text)

#     return jsonify({ 'number' : len(response_json['docs']), 'data': response_json })

if __name__ == "__main__":
    # app.run(host="127.0.0.1", port=18080, debug=True)

    PARSER = argparse.ArgumentParser(
        description="Group 1 COMP90024")

    PARSER.add_argument('--debug', action='store_true', help="Use flask debug/dev mode with file change reloading")
    ARGS = PARSER.parse_args()

    PORT = int(os.environ.get('PORT', 18080))
    HOST = "127.0.0.1"

    if ARGS.debug:
        print("Running in debug mode")
        CORS = CORS(APP)
        APP.run(host=HOST, port=PORT, debug=True)
    else:
        APP.run(host=HOST, port=PORT, debug=False)