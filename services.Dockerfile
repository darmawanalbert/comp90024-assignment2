# COMP90024 Team 1
# Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
# Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
# I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
# Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au

FROM python:3.8

WORKDIR /app

COPY services/ .

RUN pip install -r requirements.txt

CMD ["python","-u","app.py"]

# docker build -t test -f services.Dockerfile .
# docker run --name test -p 8080:8080  test:latest
# docker start test
# docker rm -vf $(docker ps -a -q) ; docker rmi -f $(docker images -a -q)
# docker rmi -f $(docker images -a -q)