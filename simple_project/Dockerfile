FROM python:3.10.3-slim-buster

ENV CONTAINER_HOME=/usr/src/app

WORKDIR $CONTAINER_HOME

ADD . $CONTAINER_HOME

RUN pip3 install -U pip
RUN pip3 install -r requirements.txt

CMD celery -A worker worker --loglevel=INFO
