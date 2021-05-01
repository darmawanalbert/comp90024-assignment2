"""The Endpoints to manage the BOOK_REQUESTS"""
import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint

from validate_email import validate_email
REQUEST_API = Blueprint('request_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


BOOK_REQUESTS = {
    "8c36e86c-13b9-4102-a44f-646015dfd981": {
        'title': u'Good Book',
        'email': u'testuser1@test.com',
        'timestamp': (datetime.today() - timedelta(1)).timestamp()
    },
    "04cfc704-acb2-40af-a8d3-4611fab54ada": {
        'title': u'Bad Book',
        'email': u'testuser2@test.com',
        'timestamp': (datetime.today() - timedelta(2)).timestamp()
    }
}

TRENDING_TOPICS = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
            [100.0, 1.0], [100.0, 0.0]
          ]
        ]
      },
      "properties": 
        { "id": 1, "top5": ["topic1", "topic2", "topic3", "topic4", "topic5"], "top5_count": [5, 4, 3, 2, 1] }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [100.0, 10.0], [101.0, 10.0], [101.0, 100.0],
            [100.0, 100.0], [100.0, 10.0]
          ]
        ]
      },
      "properties": 
        { "id": 2, "top5": ["topic11", "topic12", "topic13", "topic14", "topic15"], "top5_count": [15, 14, 13, 12, 11] }
    },
  ]
}

@REQUEST_API.route('/trending_topics', methods=['GET'])
def get_trending_topics():
    """Return all book requests
    @return: 200: an array of all known BOOK_REQUESTS as a \
    flask/response object with application/json mimetype.
    """
    return jsonify(TRENDING_TOPICS)

@REQUEST_API.route('/trending_topics/<string:_id>', methods=['GET'])
def get_trending_topics_by_id():
    """Return all book requests
    @return: 200: an array of all known BOOK_REQUESTS as a \
    flask/response object with application/json mimetype.
    """
    if _id not in TRENDING_TOPICS:
        abort(404)
    return jsonify(TRENDING_TOPICS[_id])