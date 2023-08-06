from .request import Requester
from .type import Location, Stop, Trip, Coordinate, Endpoint


class JourneyPlanner:
    def __init__(self):
        self.requester = Requester()

    def authenticate(self, username, password):
        self.requester.authenticate(username, password)

    def location(self, query):
        """Fuzzy search for stops/stations/points of interest/adresses.

        The location service can be used to perform a pattern matching of a
        user input and to retrieve a list of possible matches in the journey
        planner database. Possible matches might be stops/stations, points of
        interest and addresses.
        """
        tree = self.requester.get('locations', input=query)

        yield from (Location(element) for element in tree)

    def stopsnearby(self, *, latitude, longitude, radius=None, limit=None):
        """Find stops within a radius of a given coordinate.

        Each stop location contains the name of the
        station/stop, the coordinate, the id and the distance from the request
        coordinate in meters. All distances are as the crow flies and not
        routed.
        """
        coordinate = Coordinate(latitude=latitude, longitude=longitude)
        tree = self.requester.get('stopsNearby',
                                  coordX=coordinate.x,
                                  coordY=coordinate.y,
                                  maxRadius=radius,
                                  maxNumber=limit)

        yield from (Stop(element) for element in tree)

    def trip(self, origin, destination, *, via=None,
             date=None, time=None,
             arrivals=False,
             bus=True, metro=True, train=True):
        """The trip service calculates a trip from a specified origin to a
        specified destination. These might be stop/station IDs or coordinates
        based on addresses and points of interest validated by the location
        service or coordinates freely defined by the client.

        The parameters are named either originId or originCoordX, originCoordY,
        and originCoordName. For the destination the parameters are named either
        destId or destCoordX, destCoordY and destCoordName
        """
        endpointparams = dict()
        endpoints = dict(origin=origin, dest=destination)
        for key, endpoint in endpoints.items():
            try:
                (x, y, name) = (endpoint.x, endpoint.y, endpoint.name)
                endpointparams.update({
                    '{}CoordX'.format(key): x,
                    '{}CoordY'.format(key): y,
                    '{}CoordName'.format(key): name if name else key,
                })
            except AttributeError:
                endpointparams['{}Id'.format(key)] = endpoint

        tree = self.requester.get('trip',
                                  date=date,
                                  time=time,
                                  viaId=via,
                                  searchForArrival=int(arrivals),
                                  useBus=int(bus),
                                  useMetro=int(metro),
                                  useTrain=int(train),
                                  **endpointparams)

        yield from (Trip(element) for element in tree)

    def _stationboard(self, service, id, *, date=None, time=None,
                      bus=True, metro=True, train=True):
        """The station board board can be retrieved by the service
        departureBoard. This method will return the next 20 departures (or less
        if not existing) from a given point in time.

        In addition to departure boards the service arrivalBoard delivers
        arriving journeys at a specified stop. The parameters are identical to
        the parameters of the departureBoard service.
        """
        tree = self.requester.get(service,
                                  id=id,
                                  date=date,
                                  time=time,
                                  useBus=int(bus),
                                  useMetro=int(metro),
                                  useTrain=int(train))

        yield from tree

    def arrivalboard(self, *args, **kwargs):
        return self._stationboard('arrivalBoard', *args, **kwargs)

    def departureboard(self, *args, **kwargs):
        return self._stationboard('departureBoard', *args, **kwargs)

    def multidepartureboard(self, *ids, date=None, time=None, bus=True, metro=True, train=True):
        """The multi departure board is a combined departure board for up to 10
        different stops. It can be retrieved by a service called
        multiDepartureBoard. This method will return the next 20 departures (or
        less if not existing) of the defined stops from a given point in time.
        """
        if len(ids) > 10:
            raise Exception('MultiDepartureBoard does not support more than 10 ids')

        tree = self.requester.get('multiDepartureBoard',
                                  date=date,
                                  time=time,
                                  useBus=int(bus),
                                  useMetro=int(metro),
                                  useTrain=int(train))

        yield from tree

    def journeydetail(self, reference):
        """The journeyDetail service will deliver information about the complete
        route of a vehicle. This service can’t be called directly but only by
        reference URLs in a result of a trip or departureBoard request. It
        contains a list of all stops/stations of this journey including all
        departure and arrival times (with realtime data if available) and
        additional information like specific attributes about facilities and
        other texts.
        """
        tree = self.requester.get('journeyDetail', ref=reference)

        yield from tree
