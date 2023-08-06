from .config import BASE_URL_OPEN, BASE_URL_AUTHENTICATED
from .error import AuthenticationError, JourneyPlannerError, fromstring as errorfromstring

from xml.etree import ElementTree


from urllib.request import build_opener, HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, HTTPError
from urllib.parse import urlencode

class Requester:
    def __init__(self):
        self.baseurl = BASE_URL_OPEN
        self.opener = build_opener()

    def authenticate(self, username, password):
        manager = HTTPPasswordMgrWithDefaultRealm()
        manager.add_password(None, BASE_URL_AUTHENTICATED, username, password)
        handler = HTTPBasicAuthHandler(manager)

        self.baseurl = BASE_URL_AUTHENTICATED
        self.opener.add_handler(handler)

    def get(self, service, **params):
        tuples = sorted(params.items(), key=lambda x: x[0])
        tuples = [t for t in tuples if t[1] is not None]
        querystring = urlencode(tuples)

        url = '{}/{}?{}'.format(self.baseurl, service, querystring)

        try:
            response = self.opener.open(url)

            return _parse(response)
        except HTTPError as error:
            if error.code == 401:
                raise AuthenticationError('Invalid credentials')


def _parse(file):
    try:
        tree = ElementTree.parse(file)
        root = tree.getroot()
        errormessage = root.get('error')

        if errormessage:
            raise errorfromstring(errormessage)

        return root
    except ElementTree.ParseError:
        raise JourneyPlannerError('Invalid server response') from None
