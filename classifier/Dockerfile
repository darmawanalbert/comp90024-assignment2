FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
COPY business.txt business.txt
COPY education.txt education.txt
COPY entertainment.txt entertainment.txt
COPY places.txt places.txt
COPY politics.txt politics.txt
COPY sports.txt sports.txt
COPY cities_top50_simplified.geojson cities_top50_simplified.geojson

RUN pip install -r requirements.txt

CMD ["python","-u","tweet_harvester.py"]