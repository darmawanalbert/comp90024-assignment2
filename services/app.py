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

DB_HOST = os.environ.get('DBHOST') if os.environ.get('DBHOST') != None else "http://admin:admin@45.113.235.190:25984/"
DB_NAME = os.environ.get('DBNAME') if os.environ.get('DBNAME') != None else "comp90024_lda_scoring/"
DESIGN_LDA = "_design/lda_topic/"
VIEW_LDA = "_view/score_output"

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

def raw_lda(req_params):
    headers = {"content-type": "application/json"}
    url = f"{DB_HOST}{DB_NAME}{DESIGN_LDA}{VIEW_LDA}"

    data = json.dumps(req_params).encode('utf-8')

    scoring_data = requests.post(url, data=data, headers=headers)
    scoring_json = json.loads(scoring_data.text)

    return scoring_json

@APP.route("/lda_scoring", methods=['GET'])
@cross_origin()
def lda_scoring():
    if 'start_date' in request.args:
        _startkey = json.loads(request.args['start_date']) # [2021, 5, 9] [YYYY, M, D]
    if 'end_date' in request.args:
        _endkey = json.loads(request.args['end_date'])
    
    if _startkey:
       obj = {"startkey": [_startkey], "endkey": [_startkey, {}]} 
    elif _startkey and _endkey:
       obj = {"startkey": [_startkey], "endkey": [_endkey, {}]}
    else:
        return "Error: No start date provided. Please specify start date (and end date, if applicable)."

    scoring_json = raw_lda(obj)

    return jsonify(scoring_json["rows"])

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