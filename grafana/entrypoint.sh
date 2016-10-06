#!/usr/bin/env sh

exec /run.sh $@ &

post() {
    curl -s "http://$GF_SECURITY_ADMIN_USER:$GF_SECURITY_ADMIN_PASSWORD@localhost:3000$1" \
        -X POST \
        -H 'Content-Type: application/json;charset=UTF-8' \
        --data-binary "$2" 2> /dev/null
}

if [ ! -f "/var/lib/grafana/.init" ]; then
    until curl -s "http://$GF_SECURITY_ADMIN_USER:$GF_SECURITY_ADMIN_PASSWORD@localhost:3000/api/datasources" 2> /dev/null; do
        sleep 1
    done

    for datasource in /etc/grafana/datasources/*; do
        post "/api/datasources" "$(cat $datasource)"
    done

    for dashboard in /etc/grafana/dashboards/*; do
        post "/api/dashboards/db" "$(cat $dashboard)"
    done

    touch "/var/lib/grafana/.init"
fi

wait
