from journeyplanner import JourneyPlanner, error, Endpoint
from journeyplanner.request import _parse

from io import StringIO

import unittest

class TestService(unittest.TestCase):

    def setUp(self):
        self.jp = JourneyPlanner()

    def test_fail_authentication(self):
        jp = JourneyPlanner()
        jp.authenticate('foo', 'bar')
        with self.assertRaises(error.AuthenticationError):
            next(jp.location('elmegade 5 københavn'))

    def test_location(self):
        first = next(self.jp.location('elmegade 5 københavn'))
        self.assertEqual(first.latitude, 55.689541)
        self.assertEqual(first.longitude, 12.558038)

    def test_trip(self):
        origin=Endpoint(latitude=55.68954, longitude=12.558038)
        first = next(self.jp.trip(origin=6, destination=8000, bus=False))
        self.assertEqual(first.valid, True)

    def test_stopsnearby(self):
        first = next(self.jp.stopsnearby(latitude=55.68954, longitude=12.558038))
        self.assertEqual(first.latitude, 55.689388)

if __name__ == '__main__':
    unittest.main()
