#!/usr/bin/env python
import argparse
import logging

import Geohash
import dateutil.parser
import pytz
import requests
from influxdb import InfluxDBClient

SCHEME_IDS = {
    'all': -1,
    'cork': 2,
    'limerick': 3,
    'galway': 4
}

TZ_CORK = pytz.timezone('Europe/Dublin')


def get_response(api_key, scheme='all'):
    r = requests.post('https://data.bikeshare.ie/dataapi/resources/station/data/list',
                      headers={
                          'Content-type': 'application/x-www-form-urlencoded'
                      },
                      data={
                          'key': api_key,
                          'schemeId': SCHEME_IDS[scheme]
                      })
    r.raise_for_status()
    return r.json()


def get_station_data(api_key, scheme='all'):
    response = get_response(api_key, scheme)
    if response['responseCode'] != 0:
        raise ValueError('Unexpected response: %d %s' % (response['responseCode'], response['responseText']))
    return response['data']


def to_influxdb_point(station_data):
    return {
        'measurement': 'bikes',
        'tags': {
            'scheme_id': station_data['schemeId'],
            'scheme_name': station_data['schemeShortName'],
            'station_id': station_data['stationId'],
            'station_name': station_data['name'],
            'station_name_irish': station_data['nameIrish']
        },
        'time': TZ_CORK.localize(dateutil.parser.parse(station_data['dateStatus'], dayfirst=True)).isoformat(),
        'fields': {
            'bikes_available': station_data['bikesAvailable'],
            'docks_available': station_data['docksAvailable'],
            'docks_count': station_data['docksCount'],
            'station_status': station_data['status'],
            'latitude': float(station_data['latitude']),
            'longitude': float(station_data['longitude']),
            'geohash': Geohash.encode(float(station_data['latitude']), float(station_data['longitude']), 12)
        }
    }


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s')
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('api_key')
        parser.add_argument('username')
        parser.add_argument('password')
        parser.add_argument('--host', default='influxdb')
        parser.add_argument('--port', type=int, default=8086)
        parser.add_argument('--database', default='cork')
        args = parser.parse_args()

        # Convert the response data to InfluxDB point format
        stations = get_station_data(args.api_key, scheme='cork')
        points = list(map(to_influxdb_point, stations))

        # Connect to InfluxDB and write the data
        client = InfluxDBClient(args.host, args.port, args.username,
                                args.password, args.database)
        client.create_database(args.database)
        client.write_points(points)
    except:
        logging.exception('Could not scrape data')
