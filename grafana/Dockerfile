FROM grafana/grafana:4.4.2
MAINTAINER Donagh Horgan <me@donagh.io>

RUN apt-get update && \
    apt-get install -y curl gettext-base && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /etc/grafana
COPY dashboards ./dashboards
COPY datasources ./datasources

WORKDIR /app
COPY entrypoint.sh ./
RUN chmod u+x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
