FROM python:3.8

COPY requirements.txt /app/requirements.txt
COPY app.py /app/app.py
COPY routes /app/routes
COPY static /app/static

RUN pip install -r /app/requirements.txt

WORKDIR /app

CMD ["python","-u","/app/app.py"]