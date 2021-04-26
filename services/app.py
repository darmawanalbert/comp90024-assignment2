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

app = Flask(__name__)

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
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

DB_HOST = os.environ.get('DBHOST') if os.environ.get('DBHOST') != None else "http://admin:admin@127.0.0.1:5984/"
DB_NAME = os.environ.get('DBNAME') if os.environ.get('DBNAME') != None else "testdb"

@app.route("/",methods=["GET"])
def get():
    limit = 20
    skip = 0
    if(request.args.get('limit') != None):
        limit = request.args.get('limit')
    
    if(request.args.get('skip') != None):
        skip = request.args.get('skip')

    url = f"{DB_HOST}{DB_NAME}"
    query = {"selector": {},"limit": int(limit), "skip": int(skip)}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{url}/_find",headers=headers,data=json.dumps(query))
    response_json = json.loads(response.text)

    return jsonify({ 'number' : len(response_json['docs']), 'data': response_json })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)