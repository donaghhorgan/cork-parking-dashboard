#!/usr/bin/env python
import argparse
import Geohash
import json
import urllib

from influxdb import InfluxDBClient


URL='http://data.corkcity.ie/api/action/datastore_search'
RESOURCE_ID='c8735eb1-6da3-4dbd-9541-8995ba36a424'


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
            'free_spaces': record['free_spaces'],
            'latitude': record['latitude'],
            'longitude': record['longitude'],
            'geohash': Geohash.encode(record['latitude'], record['longitude'], 12),
            'spaces': record['spaces']
        }
    }


if __name__ == '__main__':
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

