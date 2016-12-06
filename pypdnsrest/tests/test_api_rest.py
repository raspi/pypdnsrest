import unittest

from pypdnsrest.client import PowerDnsRestApiClient


class TestWrongApiPassword(unittest.TestCase):
    def setUp(self):
        self.api = PowerDnsRestApiClient(u"wrong-password")
        self.zone = u"{0}.zone.".format(type(self).__name__.lower())
        self.nameservers = [u"ns1.".format(self.zone), u"ns2.".format(self.zone)]

    def test_create_zone(self):
        from pypdnsrest.client import PowerDnsRestApiException
        with self.assertRaises(PowerDnsRestApiException) as context:
            self.api.add_zone(self.zone, self.nameservers)
