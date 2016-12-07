import unittest

from pypdnsrest.client import PowerDnsRestApiClient


class TestApiZone(unittest.TestCase):
    def setUp(self):
        self.api = PowerDnsRestApiClient("pdnsapi")
        self.zone = "{0}.zone.".format(type(self).__name__.lower())
        self.nameservers = [
            "ns1.{0}".format(self.zone),
            "ns2.{0}".format(self.zone)
        ]

    def test_create_zone(self):
        self.assertTrue(self.api.add_zone(self.zone, self.nameservers))

    def test_delete_zone(self):
        self.assertTrue(self.api.del_zone(self.zone))

    def test_delete_zone_invalid(self):
        from pypdnsrest.client import PowerDnsRestApiException
        with self.assertRaises(PowerDnsRestApiException) as context:
            self.api.del_zone("nonexisting.")

    def test_delete_zone_invalid2(self):
        from pypdnsrest.client import PowerDnsRestApiException
        with self.assertRaises(PowerDnsRestApiException) as context:
            self.api.del_zone("nonexisting")
