import unittest

from pypdnsrest.client import PowerDnsRestApiClient
from pypdnsrest.client import PowerDnsRestApiException


class TestApiZone(unittest.TestCase):
    def setUp(self):
        self.api = PowerDnsRestApiClient(u"pdnsapi")
        self.zone = u"{0}.zone.".format(type(self).__name__.lower())
        self.nameservers = [
            u"ns1.{0}".format(self.zone),
            u"ns2.{0}".format(self.zone)
        ]

        try:
            # It's possible that failed test left old zone remains
            self.api.del_zone(self.zone)
        except Exception:
            pass

    def tearDown(self):
        try:
            self.api.del_zone(self.zone)
        except Exception:
            pass

    def test_add_zone(self):
        self.assertTrue(self.api.add_zone(self.zone, self.nameservers))

    def test_delete_zone(self):
        self.api.add_zone(self.zone, self.nameservers)
        self.assertTrue(self.api.del_zone(self.zone))

    def test_delete_zone_invalid(self):
        with self.assertRaises(PowerDnsRestApiException) as context:
            self.api.del_zone(u"nonexisting.")

    def test_delete_zone_invalid2(self):
        with self.assertRaises(PowerDnsRestApiException) as context:
            self.api.del_zone(u"nonexisting")

    def test_get_zone(self):
        from pypdnsrest.dnszone import DNSZone
        self.api.add_zone(self.zone, self.nameservers)
        self.assertIsInstance(self.api.get_zone(self.zone), DNSZone)

    def test_get_zones(self):
        self.assertIsInstance(self.api.get_zones(), list)

    def test_add_invalid(self):
        with self.assertRaises(TypeError) as context:
            self.api.add_zone(self.zone, int(1))

    def test_add_invalid2(self):
        with self.assertRaises(ValueError) as context:
            self.api.add_zone(self.zone, [])

    def test_add_invalid3(self):
        with self.assertRaises(TypeError) as context:
            self.api.add_zone(self.zone, [None])

    def test_add_invalid4(self):
        with self.assertRaises(ValueError) as context:
            self.api.add_zone(self.zone, [""])

    def test_add_invalid5(self):
        with self.assertRaises(TypeError) as context:
            self.api.add_zone(self.zone, [int(1)])
