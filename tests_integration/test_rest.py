import unittest

from pypdnsrest.client import PowerDnsRestApiClient
from pypdnsrest.client import PowerDnsRestApiException


class TestWrongApiPassword(unittest.TestCase):
    def setUp(self):
        self.api = PowerDnsRestApiClient(u"wrong-password")
        self.zone = u"{0}-rest.zone.".format(type(self).__name__.lower())
        self.nameservers = [
            u"ns1.{0}".format(self.zone),
            u"ns2.{0}".format(self.zone),
        ]

    def test_create_zone(self):
        with self.assertRaises(PowerDnsRestApiException) as context:
            self.api.add_zone(self.zone, self.nameservers)
