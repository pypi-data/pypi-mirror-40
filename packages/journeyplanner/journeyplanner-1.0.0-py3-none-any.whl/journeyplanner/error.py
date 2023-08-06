def fromstring(message):
  """Convert a Rejseplanen API error message into an appropriate exception.
  """
  error_code = message.split()[0]
  message = ERRORS.get(error_code, message)
  first_char = error_code[0]

  if first_char == 'R':
    return RestError(message)
  elif first_char == 'S':
    return ServerError(message)
  elif first_char == 'H':
    return TripServiceError(message)
  else:
    raise JourneyPlannerError(message)

#-------------------------------------------------------------------------------

ERRORS = {
  #General ReST Request Errors
  'R0001': 'Unknown service',
  'R0002': 'Invalid or missing request parameters',
  'R0007': 'Internal communication error',
  # Backend Server Errors
  'S1': 'The desired connection to the server could not be established or was not stable.',
  # Connection Request Errors
  'H9380': 'Dep./Arr./Intermed defined more than once',
  'H9360': 'Error in date field',
  'H9320': 'The input is incorrect or incomplete',
  'H9300': 'Unknown arrival station',
  'H9280': 'Unknown intermediate station',
  'H9260': 'Unknown departure station',
  'H9240': 'Unsuccessful search',
  'H9230': 'An internal error occurred',
  'H9220': 'Nearby to the given address stations could not be found',
  'H900': 'Unsuccessful or incomplete search (timetable change)',
  'H892': 'Inquiry too complex (try entering less intermediate stations)',
  'H891': 'No route found (try entering an intermediate station)',
  'H890': 'No connections found',
  'H895': 'Departure/Arrival are too near',
}

class JourneyPlannerError(Exception):
  """There was an exception that occurred while handling your request."""
  pass

class AuthenticationError(JourneyPlannerError):
    """Authentication failed."""
    pass

class RestError(JourneyPlannerError):
  """General rest error occured"""
  pass

class ServerError(JourneyPlannerError):
  """Backend Server gave error"""
  pass

class TripServiceError(JourneyPlannerError):
  """There was an error with your trip request"""
  pass
