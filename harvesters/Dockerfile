FROM python:3.8

COPY requirements.txt /app/requirements.txt
COPY twitter-api-tokens.csv /app/twitter-api-tokens.csv
COPY database/db_utils.py /app/database/db_utils.py
COPY tweet_harvester.py /app/tweet_harvester.py

RUN pip install -r /app/requirements.txt

CMD ["python","-u","/app/tweet_harvester.py"]