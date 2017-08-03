# Cork Open Data UI

A visual exploration tool for open data in Cork City, built with [Grafana](https://grafana.com) and [InfluxDB](https://influxdata.com).

Dashboards are provided for the following datasets:

- Carpark capacity
- Bikeshare station capacity
- River levels

## Requirements

To run the dashboard, you'll need the following packages:

1. [Docker Engine](https://docker.github.io/engine/installation/) >= 1.12
2. [Docker Compose](https://docker.github.io/compose/install/) >= 1.8

### Bikeshare API

Additionally, if you want to aggregate bikeshare data, you'll need an API key (just enter it in `configuration.env`). Instructions for registering for API access are available at [data.corkcity.ie](data.corkcity.ie/dataset/coca-cola-zero-bikes).

## Usage

Running the UI is easy:

1. Make sure you have all the [requirements](#Requirements) installed.
2. Customise the administration credentials and bikeshare API key in `configuration.env`.
3. Run `docker-compose up -d` to start the services.
4. Go to [localhost:3000](http://localhost:3000) to see the dashboard.

> **Note:** The dashboards will initially be empty, but the web scrapers pull data from [data.corkcity.ie](http://data.corkcity.ie) and [bikeshare.ie](https://bikeshare.ie) automatically, so it will fill out over time.
