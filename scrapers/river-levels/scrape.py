#!/usr/bin/env python
import argparse
import logging

import Geohash
import dateutil.parser
import pytz
import requests
from influxdb import InfluxDBClient

TZ_CORK = pytz.timezone('Europe/Dublin')

NAMES = {
    Geohash.encode(51.894643, -8.512962, 12): 'Lee Road',
    Geohash.encode(51.897843, -8.56668, 12): 'Angler\'s Rest'
}


def get_response(url, **params):
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_data(**params):
    data = get_response('http://data.corkcity.ie/api/action/datastore_search',
                        resource_id='1ff23e53-a0ab-4dc8-95e3-31a669547a80', **params)
    if not data['success']:
        raise ValueError('Unexpected response: %s' % data['error'])
    else:
        return data


def get_river_levels(limit=10):
    data = get_data(limit=limit)
    return data['result']['records']


def get_total_records():
    data = get_data(limit=1)
    return data['result']['total']


def to_influxdb_point(record):
    latitude = float(record['latitude'])
    longitude = float(record['longitude'])
    geohash = Geohash.encode(latitude, longitude, 12)
    return {
        'measurement': 'river-levels',
        'tags': {
            'name': NAMES[geohash]
        },
        'time': TZ_CORK.localize(dateutil.parser.parse(record['date'])).isoformat(),
        'fields': {
            'geohash': geohash,
            'latitude': latitude,
            'level': float(record['level']),
            'longitude': longitude
        }
    }


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s')
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('username')
        parser.add_argument('password')
        parser.add_argument('--host', default='influxdb')
        parser.add_argument('--port', type=int, default=8086)
        parser.add_argument('--database', default='cork')
        args = parser.parse_args()

        # Get the latest data
        records = get_river_levels()
        points = list(map(to_influxdb_point, records))

        # Connect to InfluxDB and write the data
        client = InfluxDBClient(args.host, args.port, args.username,
                                args.password, args.database)
        client.create_database(args.database)
        client.write_points(points)
    except:
        logging.exception('Could not scrape data')
