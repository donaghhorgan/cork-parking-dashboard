FROM python:2.7-alpine
MAINTAINER Donagh Horgan <me@donagh.io>

RUN pip install influxdb geohash

WORKDIR /app
COPY scrape.py scrape.cron ./
RUN crontab scrape.cron

ENTRYPOINT ["crond", "-f", "-d", "8"]
