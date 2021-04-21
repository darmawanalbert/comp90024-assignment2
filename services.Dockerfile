FROM python:3.8

COPY services/ /app/

RUN pip install -r /app/requirements.txt

CMD ["python","-u","/app/app.py"]