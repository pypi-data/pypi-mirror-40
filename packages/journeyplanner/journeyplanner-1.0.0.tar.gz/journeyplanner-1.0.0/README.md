# Journeyplanner

## Installation
The journeyplanner library can be installed using pip:

    $ pip install journeyplanner

### Examples
```
client = JourneyPlanner()
dt = datetime(2019, 1, 8, 12, 0, 0)
origin = Endpoint(latitude=55.68325233, longitude=12.57150292, name="noerreport")
destination = Endpoint(latitude=55.67271128, longitude=12.56635308, name="hovedbanen")
trip = client.trip(origin, destination, date=dt.date(), time=dt.time())
print(list(trip))
```

### Authentication
```
client = JourneyPlanner()
client.authenticate('USERNAME', 'PASSWORD')
```

## API reference

### Trip objects
Trip instances have the following attributes:

#### `Trip.legs`
  List of leg instances

### Leg objects
Leg instances have the following attributes:

* `Leg.name`
* `Leg.type`
* `Leg.origin`
* `Leg.destination`
* `Leg.notes`
