FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential python-flask sqlite3 libsqlite3-dev
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
#ENTRYPOINT ["python","-m","flask","run"]
CMD python -m flask run --host=0.0.0.0
