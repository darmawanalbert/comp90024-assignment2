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

import scipy
import numpy as np
import argparse
import calendar

from scipy import stats
from flask_cors import CORS, cross_origin
from datetime import date, datetime, timedelta

APP = Flask(__name__)
CORS = CORS(APP, resources={r"/*": {"origins": "*"}})

DB_HOST = os.environ.get('DBHOST') if os.environ.get('DBHOST') != None else "http://admin:admin@45.113.235.190:25984/"
DB_NAME_LDA = os.environ.get('DB_NAME_LDA') if os.environ.get('DB_NAME_LDA') != None else "comp90024_lda_scoring/"
DB_NAME_HARVEST = os.environ.get('DB_NAME_HARVEST') if os.environ.get('DB_NAME_HARVEST') != None else "comp90024_tweet_harvest/"
DESIGN_LDA = "_design/lda_topic/"
DESIGN_HARVEST = ''
VIEW_LDA = "_view/score_output"
VIEW_HARVEST = ''

@APP.route("/cities", methods=["GET"])
@cross_origin()
def cities():
    path = "./data/cities_top50_simplified.geojson"
    with open(path) as f:
        data = json.load(f)

    return jsonify(data)

@APP.route("/lda-scores", methods=['GET'])
@cross_origin()
def lda_scoring():
    start_temp = [0,0,0]
    if 'start_date' in request.args:
        start_date = request.args['start_date']
    else:
        start_date = str(date.today() - timedelta(days=1))
    
    for i in range(len(start_temp)):
        start_temp[i] = int(start_date.split('-')[i])
    _startkey = start_temp
    
    end_temp = [0,0,0]
    if 'end_date' in request.args:
        end_date = request.args['end_date']
        if datetime.strptime(end_date, '%Y-%m-%d') < datetime.strptime(start_date, '%Y-%m-%d'):
            return "End date must be after start date."
        for i in range(len(end_temp)):
            end_temp[i] = int(end_date.split('-')[i])
        _endkey = end_temp
    
    if _startkey:
       obj = {"startkey": [_startkey], "endkey": [_startkey, {}]}
    elif _startkey and _endkey:
       obj = {"startkey": [_startkey], "endkey": [_endkey, {}]}
    else:
        return "Error: No start date provided. Please specify a start date (and end date, if applicable)."

    scoring_json = raw_lda(obj)

    return jsonify(scoring_json["rows"])

@APP.route('/charts', methods=['GET'])
@cross_origin()
def analysis_id():
    start_temp = [0,0,0]
    if 'start_month' in request.args:
        start_month = request.args['start_month']
    else:
        start_month = str(date.today().strftime("%Y-%m"))
    
    start_date = start_month + '-' + "1"
    
    for i in range(len(start_temp)):
        start_temp[i] = int(start_date.split('-')[i])
    _startkey = start_temp
    
    end_temp = [0,0,0]
    if 'end_month' in request.args:
        end_month = request.args['end_month']
        if datetime.strptime(end_month, '%Y-%m') < datetime.strptime(start_month, '%Y-%m'):
            return "End month must be after start month."
        last_day = calendar.monthrange(end_month.split('-')[0], end_month.split('-')[1])[1]
    else:
        end_month = start_month
        last_day = calendar.monthrange(int(end_month.split('-')[0]), int(end_month.split('-')[1]))[1]
    
    end_date = end_month + '-' + str(last_day)
    for i in range(len(end_temp)):
        end_temp[i] = int(end_date.split('-')[i])
    _endkey = end_temp
    
    if _startkey:
       obj = {"startkey": [_startkey], "endkey": [_endkey, {}]}
    else:
        return "Error: No start date provided. Please specify a start date (and end date, if applicable)."
    
    lda_scores = raw_lda(obj)["rows"]
    lda_aggregate = aggregated_lda(lda_scores)
    
    ID = 'id'
    VALUE = 'value'
    all_analysis = []
    
    income_analysis = {}
    income_analysis[ID] = 'income'
    income_analysis[VALUE] = analysis(lda_aggregate, median_income())
    all_analysis.append(income_analysis)

    unemployment_analysis = {}
    unemployment_analysis[ID] = 'unemployment'
    unemployment_analysis[VALUE] = analysis(lda_aggregate, unemployment())
    all_analysis.append(unemployment_analysis)
    
    age_analysis = {}
    age_analysis[ID] = 'age'
    age_analysis[VALUE] = analysis(lda_aggregate, age())
    all_analysis.append(age_analysis)

    return jsonify(all_analysis)

def raw_lda(req_params):
    headers = {"content-type": "application/json"}
    url = f"{DB_HOST}{DB_NAME_LDA}{DESIGN_LDA}{VIEW_LDA}"

    data = json.dumps(req_params).encode('utf-8')

    scoring_data = requests.post(url, data=data, headers=headers)
    scoring_json = json.loads(scoring_data.text)

    return scoring_json

def analysis(topic_scores, ucl):
    X_COOR = 'x'
    Y_COOR = 'y'
    GRADIENT = 'm'
    Y_INTERCEPT = 'c'
    R_SQUARED = 'r_squared'
    P_VAL = 'p_val'
    STD_ERR = 'std_err'

    topic_dct = {}

    for city, dct in topic_scores.items():
        for topic, v in dct["topics"].items():
            if topic not in topic_dct:
                topic_dct[topic] = {}
                topic_dct[topic][X_COOR] = []
                topic_dct[topic][Y_COOR] = []
                topic_dct[topic][GRADIENT] = 0
                topic_dct[topic][Y_INTERCEPT] = 0
            topic_dct[topic][X_COOR].append(ucl[city])
            topic_dct[topic][Y_COOR].append(v)

    for k, val in topic_dct.items():
        min_x = min(val[X_COOR])
        max_x = max(val[X_COOR])
        min_y = min(val[Y_COOR])
        max_y = max(val[Y_COOR])
        temp_x = [(val - min_x) / (max_x - min_x) for val in val[X_COOR]]
        temp_y = [(val - min_y) / (max_y - min_y) for val in val[Y_COOR]]
        val[X_COOR] = temp_x
        val[Y_COOR] = temp_y

    for topic, val in topic_dct.items():
        x_np = np.array(val[X_COOR])
        y_np = np.array(val[Y_COOR])
        val[GRADIENT], val[Y_INTERCEPT], r_value, val[P_VAL], val[STD_ERR] = scipy.stats.linregress(
            x_np, y_np)
        val[R_SQUARED] = r_value**2
    
    return topic_dct

def aggregated_lda(lda_scores):
    BIZ = 'business'
    EDU = 'education'
    ENTERTAINMENT = 'entertainment'
    PLACES = 'places'
    POL = 'politics'
    SPORT = 'sport'
    TWT_COUNT = 'tweets_count'
    TOPICS = 'topics'
    name_dct = ucl_name_to_code()
    lda_dct = {}
    
    for score in lda_scores:
        ucl_code = name_dct[score["key"][1]]
        if ucl_code not in lda_dct:
            lda_dct[ucl_code] = {TOPICS: {}, TWT_COUNT: 0}
            lda_dct[ucl_code][TOPICS] = {BIZ: 0, EDU: 0, ENTERTAINMENT: 0, PLACES: 0, POL: 0, SPORT: 0}
            lda_dct[ucl_code][TWT_COUNT] = 0
        lda_dct[ucl_code][TWT_COUNT] += int(score['value'][TWT_COUNT])
        for k, v in score['value']['topic_score'].items():
            lda_dct[ucl_code][TOPICS][k] += int(v)
    
    for dct in lda_dct.values():
        for k, v in dct[TOPICS].items():
            dct[TOPICS][k] = v / dct[TWT_COUNT]

    return lda_dct

def ucl_name_to_code():
    path = "./data/cities_top50_simplified.geojson"
    with open(path) as f:
        data = json.load(f)
    
    name_dct = {}
    for feature in data["features"]:
        code = feature["properties"]["UCL_CODE_2016"]
        name = feature["properties"]["UCL_NAME_2016"].lower()
        name_dct[name] = str(code)

    return name_dct

def median_income():
    sa2_aggregate = "./data/sa2_aggregate.json"
    path = "./data/SA2-G02_Selected_Medians_and_Averages-Census_2016.json"

    MED_WEEKLY_INC = 'median_tot_prsnl_inc_weekly'
    TOT_MED_WEEKLY_INC = 'cumul_med_weekly_inc'
    AVG_MED_WEEKLY_INC = 'avg_med_weekly_inc'
    SA2_ID = 'sa2_main16'
    
    ucl_income = {}
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
        ucl_income[k] = temp_dict[AVG_MED_WEEKLY_INC]

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

    ucl_unemployment = {}
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
        ucl_unemployment[k] = temp_dict[PERCENTAGE_UNEMPLOYED]

    return ucl_unemployment

def age():
    sa2_aggregate = "./data/sa2_aggregate.json"
    path = "./data/SA2-G01_Selected_Person_Characteristics_by_Sex-Census_2016.json"

    ucl_age = {}
    temp_age = {}
    
    SA2_ID = 'sa2_main16'
    AGE_25_34_COUNT = 'age_25_34_yr_p'
    POP_COUNT = 'tot_p'
    
    PROP_AGE_25_34 = 'proportion_age_25_34'
    
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
        ucl_age[k] = temp_dict[PROP_AGE_25_34]

    return ucl_age

@APP.route("/")
@cross_origin()
def home():
    test_db_connection = raw_lda({"startkey": [2021, 5, 9], "endkey": [{}, 2021, 5, 9]})

    return jsonify(test_db_connection)
    
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
