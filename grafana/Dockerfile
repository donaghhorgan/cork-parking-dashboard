FROM grafana/grafana:4.1.1
MAINTAINER Donagh Horgan <me@donagh.io>

RUN apt-get update && \
    apt-get install -y curl gettext-base && \
    rm -rf /var/lib/apt/lists/*

COPY dashboards /etc/grafana/dashboards
COPY datasources /etc/grafana/datasources

WORKDIR /app
COPY entrypoint.sh ./
RUN chmod u+x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
