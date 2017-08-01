#!/usr/bin/env python
import argparse
import json
import logging
import urllib

import Geohash
from influxdb import InfluxDBClient

URL = 'http://data.corkcity.ie/api/action/datastore_search'
RESOURCE_ID = '6cc1028e-7388-4bc5-95b7-667a59aa76dc'


def to_get_request(url, **kwargs):
    return url + '?' + urllib.urlencode(kwargs)


def to_influxdb_point(record):
    return {
        'measurement': 'carpark',
        'tags': {
            'identifier': record['identifier'],
            'name': record['name'],
            'notes': record['notes'],
            'opening_times': record['opening_times']
        },
        'time': record['date'],
        'fields': {
            'free_spaces': int(record['free_spaces']),
            'latitude': float(record['latitude']),
            'longitude': float(record['longitude']),
            'geohash': Geohash.encode(float(record['latitude']), float(record['longitude']), 12),
            'spaces': int(record['spaces'])
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

        # Request the latest data
        url = to_get_request(URL, resource_id=RESOURCE_ID)
        response = urllib.urlopen(url)

        # Convert the response data to InfluxDB point format
        data = json.loads(response.read().decode('utf-8'))
        points = list(map(to_influxdb_point, data['result']['records']))

        # Connect to InfluxDB and write the data
        client = InfluxDBClient(args.host, args.port, args.username,
                                args.password, args.database)
        client.create_database(args.database)
        client.write_points(points)
    except:
        logging.exception('Could not scrape data')
