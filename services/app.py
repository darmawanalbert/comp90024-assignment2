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
from flask_cors import CORS, cross_origin
# from routes import request_api

APP = Flask(__name__)
CORS = CORS(APP, resources={r"/*": {"origins": "*"}})

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

@APP.route("/cities", methods=["GET"])
@cross_origin()
def cities():
    path = "./data/cities_top50_simplified.geojson"
    with open(path) as f:
        data = json.load(f)

    return jsonify(data)

@APP.route('/charts/all', methods=['GET'])
@cross_origin()
def analysis_all():
    path = "./data/chart1.json"

    with open(path) as f:
        data = json.load(f)

    return jsonify(data)

@APP.route('/charts', methods=['GET'])
@cross_origin()
def analysis_id():
    path = "./data/chart1.json"

    if 'id' in request.args:
        _id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."

    results = []
    with open(path) as f:
        charts = json.load(f)
        for chart in charts:
            if chart['id'] == _id:
                results.append(chart)

    return jsonify(results)

def median_income():
    sa2_aggregate = "./data/sa2_aggregate.json"
    path = "./data/SA2-G02_Selected_Medians_and_Averages-Census_2016.json"

    MED_WEEKLY_INC = 'median_tot_prsnl_inc_weekly'
    TOT_MED_WEEKLY_INC = 'cumul_med_weekly_inc'
    AVG_MED_WEEKLY_INC = 'avg_med_weekly_inc'
    SA2_ID = 'sa2_main16'
    
    ucl_income = []
    temp_income = {}
    with open(path) as path:
        sa2_json = json.load(path)
        sa2_all = sa2_json['features']
    
    with open(sa2_aggregate) as f:
        aggregate = json.load(f)
    
    for k,v in aggregate.items():
        temp_income[k] = {}
        temp_income[k][TOT_MED_WEEKLY_INC] = 0
        temp_income[k][AVG_MED_WEEKLY_INC] = 0
        for sa2 in v:
            for sa2_data in sa2_all:
                if sa2_data['properties'][SA2_ID] == sa2:
                    med_weekly_inc = sa2_data['properties'][MED_WEEKLY_INC]
                    temp_income[k][TOT_MED_WEEKLY_INC] += med_weekly_inc
    
    UCL_CODE_2016 = 'UCL_CODE_2016'
    temp_dict = {}
    for k,v in temp_income.items():
        temp_dict = {}
        temp_dict[UCL_CODE_2016] = k
        temp_dict[AVG_MED_WEEKLY_INC] = temp_income[k][TOT_MED_WEEKLY_INC] / len(aggregate[k])
        ucl_income.append(temp_dict)

    return ucl_income

@APP.route('/median_income/all', methods=['GET'])
@cross_origin()
def median_income_all():
    ucl_income = median_income()

    return jsonify(ucl_income)

@APP.route('/median_income', methods=['GET'])
@cross_origin()
def median_income_id():
    
    ucl_income = median_income()
    UCL_CODE_2016 = 'UCL_CODE_2016'

    if 'id' in request.args:
        _id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."

    for ucl in ucl_income:
        if ucl[UCL_CODE_2016] == _id:
            return jsonify(ucl)

def unemployment():
    sa2_aggregate = "./data/sa2_aggregate.json"
    path = "./data/SA2-G40_Selected_Labour_Force__Education_and_Migration_Characteristics_by_Sex-Census_2016.json"

    PERCENT_UNEMPLOYMENT = 'percent_unem_loyment_p'
    TOTAL_POP = 'lfs_tot_lf_p'
    TOTAL_UNEMPLOYMENT = 'total_unemployment'
    SA2_ID = 'sa2_main16'
    TOT_LABOUR_FORCE = 'tot_lf'
    PERCENTAGE_UNEMPLOYED = 'unemployment_rate'

    ucl_unemployment = []
    temp_unemployment = {}
    with open(path) as path:
        sa2_json = json.load(path)
        sa2_all = sa2_json['features']
    
    with open(sa2_aggregate) as f:
        aggregate = json.load(f)
    
    for k,v in aggregate.items():
        temp_unemployment[k] = {}
        temp_unemployment[k][TOTAL_UNEMPLOYMENT] = 0
        temp_unemployment[k][TOT_LABOUR_FORCE] = 0
        for sa2 in v:
            for sa2_data in sa2_all:
                if sa2_data['properties'][SA2_ID] == sa2:
                    tot_unemployed = (sa2_data['properties'][PERCENT_UNEMPLOYMENT] / 100) * sa2_data['properties'][TOTAL_POP]
                    temp_unemployment[k][TOTAL_UNEMPLOYMENT] += tot_unemployed
                    temp_unemployment[k][TOT_LABOUR_FORCE] += sa2_data['properties'][TOTAL_POP]
    
    UCL_CODE_2016 = 'UCL_CODE_2016'
    for k,v in temp_unemployment.items():
        temp_dict = {}
        temp_dict[UCL_CODE_2016] = k
        temp_dict[PERCENTAGE_UNEMPLOYED] = temp_unemployment[k][TOTAL_UNEMPLOYMENT] / temp_unemployment[k][TOT_LABOUR_FORCE]
        temp_dict[TOT_LABOUR_FORCE] = temp_unemployment[k][TOT_LABOUR_FORCE]
        ucl_unemployment.append(temp_dict)

    return ucl_unemployment

@APP.route('/unemployment_rate/all', methods=['GET'])
@cross_origin()
def unemployment_all():
    ucl_unemployment = unemployment()

    return jsonify(ucl_unemployment)

@APP.route('/unemployment_rate', methods=['GET'])
@cross_origin()
def unemployment_id():
    ucl_unemployment = unemployment()

    UCL_CODE_2016 = 'UCL_CODE_2016'

    if 'id' in request.args:
        _id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."

    for ucl in ucl_unemployment:
        if ucl[UCL_CODE_2016] == _id:
            return jsonify(ucl)

def age():
    # Database access, later delete
    headers = {"content-type": "application/json"}
    url = "http://admin:admin@45.113.235.136:15984/comp90024_tweet_harvest/_design/topic_modelling/_view/count_by_place"

    obj = {"startkey": [[2021, 5, 9]], "endkey": [[2021, 5, 9], {}], "group": True}
    data = json.dumps(obj).encode('utf-8')

    count_data = requests.post(url, data=data, headers=headers)
    count_json = count_data.text
    count_dict = json.loads(count_json)
    # End of database access

    sa2_aggregate = "./data/sa2_aggregate.json"
    path = "./data/SA2-G01_Selected_Person_Characteristics_by_Sex-Census_2016.json"

    ucl_age = []
    temp_age = {}
    
    SA2_ID = 'sa2_main16'
    AGE_25_34_COUNT = 'age_25_34_yr_p'
    POP_COUNT = 'tot_p'
    
    PROP_AGE_25_34 = 'proportion_age_25_34'
    TOTAL_POP = 'total_pop'

    with open(path) as path:
        sa2_json = json.load(path)
        sa2_all = sa2_json['features']
    
    with open(sa2_aggregate) as f:
        aggregate = json.load(f)
    
    for k,v in aggregate.items():
        temp_age[k] = {}
        temp_age[k][AGE_25_34_COUNT] = 0
        temp_age[k][POP_COUNT] = 0
        for sa2 in v:
            for sa2_data in sa2_all:
                if sa2_data['properties'][SA2_ID] == sa2:
                    temp_age[k][AGE_25_34_COUNT] += sa2_data['properties'][AGE_25_34_COUNT]
                    temp_age[k][POP_COUNT] += sa2_data['properties'][POP_COUNT]
    
    UCL_CODE_2016 = 'UCL_CODE_2016'
    for k,v in temp_age.items():
        temp_dict = {}
        temp_dict[UCL_CODE_2016] = k
        temp_dict[PROP_AGE_25_34] = temp_age[k][AGE_25_34_COUNT] / temp_age[k][POP_COUNT]
        temp_dict[POP_COUNT] = temp_age[k][POP_COUNT]
        ucl_age.append(temp_dict)

    return ucl_age


@APP.route("/age_25_34/all", methods=['GET'])
@cross_origin()
def age_all():
    ucl_age = age()
    return jsonify(ucl_age)

@APP.route('/age_25_34', methods=['GET'])
@cross_origin()
def age_id():
    ucl_age = age()

    UCL_CODE_2016 = 'UCL_CODE_2016'

    if 'id' in request.args:
        _id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."

    for ucl in ucl_age:
        if ucl[UCL_CODE_2016] == _id:
            return jsonify(ucl)

@APP.route("/")
@cross_origin()
def home():
    headers = {"content-type": "application/json"}
    url = "http://admin:admin@45.113.235.136:15984/comp90024_tweet_harvest/_design/topic_modelling/_view/count_by_place"

    obj = {"startkey": [[2021, 5, 9]], "endkey": [[2021, 5, 9], {}], "group": True}
    data = json.dumps(obj).encode('utf-8')

    count_data = requests.post(url, data=data, headers=headers)
    count_json = count_data.text
    count_dict = json.loads(count_json)

    return jsonify(count_dict)
    
if __name__ == "__main__":
    # app.run(host="127.0.0.1", port=18080, debug=True)
    PARSER = argparse.ArgumentParser(
        description="Group 1 COMP90024")

    PARSER.add_argument('--debug', action='store_true', help="Use flask debug/dev mode with file change reloading")
    ARGS = PARSER.parse_args()

    PORT = int(os.environ.get('PORT', 8080))
    HOST = "0.0.0.0"

    if ARGS.debug:
        print("Running in debug mode")
        APP.run(host=HOST, port=PORT, debug=True)
    else:
        APP.run(host=HOST, port=PORT, debug=False)

# Wildan's for reference
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