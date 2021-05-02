# COMP90024 Team 1
# Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
# Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
# I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
# Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au

from flask import Flask, jsonify, request
import requests
import os
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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
    app.run(host="0.0.0.0", port=8080, debug=True)