FROM python:3.6-alpine3.8 

COPY kafka kafka
COPY requirements.txt streamer.py ./

RUN apk update && apk upgrade && apk add bash && apk --update add openjdk8

RUN pip install -r requirements.txt

RUN python streamer.py
