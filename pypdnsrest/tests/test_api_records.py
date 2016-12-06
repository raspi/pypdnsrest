import unittest

from pypdnsrest.client import PowerDnsRestApiClient


class TestApiRecords(unittest.TestCase):
    def setUp(self):
        self.api = PowerDnsRestApiClient("pdnsapi")
        self.zone = "{0}.zone.".format(type(self).__name__.lower())
        self.nameservers = ["ns1.".format(self.zone), "ns2.".format(self.zone)]
        self.api.add_zone(self.zone, self.nameservers)

    def tearDown(self):
        self.api.del_zone(self.zone)

    def test_create_record_a(self):
        from ipaddress import IPv4Address
        from pypdnsrest.dnsrecords import DNSARecord
        rec = DNSARecord(self.zone)
        rec.set_data(IPv4Address("192.168.101.1"))
        self.assertTrue(self.api.add_record(self.zone, rec))

    def test_create_record_aaaa(self):
        from ipaddress import IPv6Address
        from pypdnsrest.dnsrecords import DNSAaaaRecord
        rec = DNSAaaaRecord(self.zone)
        rec.set_data(IPv6Address("fd00::"))
        self.assertTrue(self.api.add_record(self.zone, rec))
