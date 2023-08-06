from . import JourneyPlanner

import argparse

parser = argparse.ArgumentParser(prog='python -m journeyplanner', description='Make requests to the journeyplanner API')

parser.add_argument('-u', help='authenticate request')
parser.add_argument('-p', help='authenticate request')

subparsers = parser.add_subparsers(help='api service', dest='service')

parser_location = subparsers.add_parser('location', help='location service')
parser_location.add_argument('query', type=str, help='the search query')

parser_trip = subparsers.add_parser('trip', help='trip service')
exorigin = parser_trip.add_mutually_exclusive_group(required=True)
exorigin.add_argument('--originid', type=int, help='origin')
exorigin.add_argument('--origin', nargs=2, type=float, metavar=('LATITUDE', 'LONGITUDE'))
exdest = parser_trip.add_mutually_exclusive_group(required=True)
exdest.add_argument('--destinationid', type=int, help='destination')
exdest.add_argument('--destination', nargs=2, type=float, metavar=('LATITUDE', 'LONGITUDE'))

parser_stopsnearby = subparsers.add_parser('stopsnearby', help='stops nearby service')
parser_stopsnearby.add_argument('latitude', type=float, help='latitude')
parser_stopsnearby.add_argument('longitude', type=float, help='longitude')

jp = JourneyPlanner()
args = parser.parse_args()
if args.u and args.p:
    jp.authenticate(args.u, args.p)

if args.service == 'location':
    for x in jp.location(args.query):
        print(str(x))

if args.service == 'stopsnearby':
    for x in jp.stopsnearby(latitude=args.latitude, longitude=args.longitude, radius=10000):
        print(str(x))

if args.service == 'trip':
    origin = args.originid if args.originid else args.origin
    destination = args.destinationid if args.destinationid else args.destination

    for x in jp.trip(origin=origin, destination=destination):
        print(str(x))
