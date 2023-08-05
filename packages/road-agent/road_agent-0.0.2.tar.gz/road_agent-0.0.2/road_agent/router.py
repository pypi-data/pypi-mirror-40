from LatLon import LatLon, Latitude, Longitude
import requests
from time import sleep


def split(s, t, speed):
    """
    This function will return a list of points between source and
    target points.

    :return: list of points between s(ource) and t(arget) at intervals
             of size @speed

    :param s: source point
    :param t: target point
    :param speed: speed in m/s
    :type s: tuple of floats, order must be (lon, lat)
    :type t: tuple of floats, order must be (lon, lat)

    """
    s = LatLon(Latitude(s[1]),
               Longitude(s[0]))

    t = LatLon(Latitude(t[1]),
               Longitude(t[0]))

    heading = s.heading_initial(t)

    fine = [(s.lon.decimal_degree,
             s.lat.decimal_degree), ]
    p = s

    while True:
        step = p.offset(heading,
                        speed / 1000.0)

        if step.distance(t) * 1000.0 > speed * 1.2:
            fine.append((step.lon.decimal_degree,
                         step.lat.decimal_degree))
            p = step
        else:
            fine.append((t.lon.decimal_degree,
                         t.lat.decimal_degree))
            break

    return fine


def refine(route, speed):
    """
    Returns a finer-grain route, splitting it at @speed intervals.

    :param route: list of tuples of (lon, lat)
    :param speed: interval at which route will be refined

    :return: list of (lon, lat) tuples
    """

    if len(route) == 0:
        return []

    fine = []
    for i in range(len(route)-1):
        fine += split(route[i], route[i + 1], speed)[1:-1]
    fine.append(route[-1])
    return fine


def route_from_geojson(geojson):
    """
    extracts the coordinates list from BRouter's geojson

    :param geojson: full response of BRouter server
    """
    return [(c[0], c[1])
            for c in geojson['features'][0]['geometry']['coordinates']]


def length_from_geojson(geojson):
    """
    return track-length in metres, reported by BRouter
    """
    return int(geojson['features'][0]['properties']['track-length'])


class Router:
    """
    This class uses the requests library to query a BRouter server.
    """

    def __init__(self,
                 protocol='http', host='localhost', port=17777,
                 profile='trekking'):
        self.route_url = "{protocol}://{host}:{port}/brouter".format(
            protocol=protocol,
            host=host,
            port=port)
        self.length = 0
        self.profile = profile
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=100,
                                                pool_maxsize=100)
        self.session.mount('http://', adapter)

    def get_raw_route(self, points):
        """
        Use brouter server to get route thru points. @points should at
        least contain a source tuple and a destination tuple.

        :param points: list of (lon, lat) tuples
        :return: list of (lon, lat) tuples with the route connecting
                 supplied points

        .. note:: if BRouter throws an error will return an empty route.
                  See BRouter log to debug.
        """
        lonlats = u"|".join(["%s,%s" % (p.lon, p.lat)
                             for p in points])
        params = "?lonlats=%s&alternativeidx=0&profile=%s&format=geojson" % (
            lonlats, self.profile)

        response = self.session.get(self.route_url + params)

        try:
            geojson = response.json()
            self.length = length_from_geojson(geojson)
            return route_from_geojson(geojson)
        except ValueError:
            # if BRouter throws an error, just return an empty route
            sleep(0.1)
            return []

    def get_route(self, points, speed=None):
        """If @speed is given, return refined route. Else: return raw route.

        :param points: list of (lon, lat). Should at least contain a
                       source tuple and a destination tuple, but may
                       contain other points inbetween
        :param speed: in m/s

        :return: list of (lon, lat) tuples with route, refined if
                 speed supplied, or output of get_raw_route

        """
        if speed:
            return refine(self.get_raw_route(points),
                          speed)
        else:
            return self.get_raw_route(points)
