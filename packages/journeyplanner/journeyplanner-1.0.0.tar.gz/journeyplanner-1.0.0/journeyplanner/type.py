from . import config

from datetime import date, time, datetime

def parsedatetime(date, time):
    """# DD.MM.YY, HH:MM"""
    return datetime.strptime('{}-{}'.format(date, time), '%d.%m.%y-%H:%M')


class Coordinate():
    """Journey Planner coordinate.
    Converts between internal xy coords and regular lat/lon
    """
    def __init__(self, *, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    @property
    def x(self):
        return self._z(self.longitude)

    @property
    def y(self):
        return self._z(self.latitude)

    @staticmethod
    def _z(foo):
        return int(foo * config.COORDINATE_MULTIPLIER)

    @classmethod
    def fromxy(cls, *, x, y):
        return cls(latitude=y / config.COORDINATE_MULTIPLIER,
                   longitude=x / config.COORDINATE_MULTIPLIER)

class Endpoint(Coordinate):
    def __init__(self, *, latitude, longitude, name=None):
        super().__init__(latitude=latitude, longitude=longitude)
        self.name = name

class Resource:
    def __repr__(self):
        return repr(self.__dict__)

class Location(Resource):
    def __init__(self, element):
        self.name = element.get('name')
        coordinate = Coordinate.fromxy(y=int(element.get('y')),
                                       x=int(element.get('x')))
        self.latitude = coordinate.latitude
        self.longitude = coordinate.longitude

        if element.tag == 'StopLocation':
            self.type = 'stop'
            self.id = int(element.get('id'))

        if element.tag == 'CoordLocation':
            self.id = None
            if element.get('type') == 'ADR':
                self.type = 'address'
            if element.get('type') == 'POI':
                self.type = 'poi'


class Stop(Resource):
    def __init__(self, element):
        self.id = int(element.get('id'))
        self.name = element.get('name')
        c = Coordinate.fromxy(y=int(element.get('y')),
                                       x=int(element.get('x')))
        (self.latitude, self.longitude) = (c.latitude, c.longitude)

        try:
            self.distance = int(element.get('distance'))
        except ValueError:
            self.distance = None


class LegEndpoint(Resource):
    def __init__(self, element):
        try:
            self.datetime = parsedatetime(element.get('rtDate'), element.get('rtTime'))
        except:
            self.datetime = parsedatetime(element.get('date'), element.get('time'))

        self.name = element.get('name')
        self.type = element.get('type')
        self.track = element.get('track')
        self.realtrack = element.get('rtTrack')

    @property
    def delayed(self):
        return self.realtime.datetime


class Leg(Resource):
    def __init__(self, leg):
        self.raw = leg.attrib
        self.name = leg.get('name')
        self.type = leg.get('type')

        self.origin = LegEndpoint(leg.find('Origin'))
        self.destination = LegEndpoint(leg.find('Destination'))

        try:
            self.notes = leg.find('Notes').get('text')
        except AttributeError:
            self.notes = None

        try:
            self.ref = leg.find('JourneyDetailRef').get('ref')
        except AttributeError:
            self.ref = None

    @property
    def duration(self):
        """Leg travel duration.
        """
        return self.destination.datetime - self.origin.datetime


class Trip(Resource):
    def __init__(self, element):
        self.alternative = element.get('alternative', False)
        self.valid = element.get('valid', True)
        self.legs = [Leg(leg) for leg in element]

    @property
    def duration(self):
        """Duration of entire trip.
        """
        durations = iter(leg.duration for leg in self.legs)
        first = next(durations)
        return sum(durations, first)
