# Cork City Parking Dashboard

A dashboard for parking data in Cork City, built with [Grafana](https://grafana.net) and [InfluxDB](https://influxdata.com).

## Requirements

To run the dashboard, you'll need the following packages:

1. [Docker Engine](https://docker.github.io/engine/installation/) >= 1.12
2. [Docker Compose](https://docker.github.io/compose/install/) >= 1.8

## Usage

Running the dashboard is easy:

1. Make sure you have all the [requirements](#Requirements) installed.
2. Customise the administration credentials in `configuration.env`.
3. Run `docker-compose up -d` to start the services.
4. Go to [localhost:3000](http://localhost:3000) to see the dashboard.

> **Note:** The dashboard will initially be empty, but the web scraper pulls data from [data.corkcity.ie](http://data.corkcity.ie) once a minute, so it will fill out over time.
