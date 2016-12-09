import unittest

from pypdnsrest.client import PowerDnsRestApiClient
from  pypdnsrest.dnsrecords import InvalidDNSRecordException


class TestApiRecords(unittest.TestCase):
    def setUp(self):
        self.api = PowerDnsRestApiClient(u"pdnsapi")
        self.zone = u"{0}.zone.".format(type(self).__name__.lower())
        self.nameservers = [
            u"ns1.{0}".format(self.zone),
            u"ns2.{0}".format(self.zone),
        ]

        try:
            # It's possible that failed test left old zone remains
            self.api.del_zone(self.zone)
        except:
            pass

        self.api.add_zone(self.zone, self.nameservers)

    def tearDown(self):
        self.api.del_zone(self.zone)

    def test_add_record_soa(self):
        from pypdnsrest.dnsrecords import DNSSoaRecord
        from pypdnsrest.dnsrecords import DNSSoaRecordData

        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), 1)

        rec = DNSSoaRecord(self.zone)
        rec.set_data(soadata)
        self.assertTrue(self.api.add_record(self.zone, rec))

    def test_add_record_a(self):
        from ipaddress import IPv4Address
        from pypdnsrest.dnsrecords import DNSARecord
        rec = DNSARecord(self.zone)
        rec.set_data(IPv4Address(u"192.168.101.1"))
        self.assertTrue(self.api.add_record(self.zone, rec))

    def test_add_record_aaaa(self):
        from ipaddress import IPv6Address
        from pypdnsrest.dnsrecords import DNSAaaaRecord
        rec = DNSAaaaRecord(self.zone)
        rec.set_data(IPv6Address(u"fd12:3456:789a:bcde:f012:3456:789a:bcde"))
        self.assertTrue(self.api.add_record(self.zone, rec))

    def test_2nameservers(self):
        from pypdnsrest.dnsrecords import DNSNsRecord

        rec = DNSNsRecord(self.zone)
        rec.set_data("ns1.{0}".format(self.zone))
        self.api.add_record(self.zone, rec)

        rec = DNSNsRecord(self.zone)
        rec.set_data("ns2.{0}".format(self.zone))
        self.assertTrue(self.api.add_record(self.zone, rec))

    def test_add_record_invalid(self):
        with self.assertRaises(TypeError) as context:
            self.api.add_record(self.zone, u"invalid")

    def test_add_record_invalid2(self):
        from pypdnsrest.dnsrecords import DNSARecord
        rec = DNSARecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            self.api.add_record(self.zone, rec)

    def test_delete_record(self):
        from ipaddress import IPv4Address
        from pypdnsrest.dnsrecords import DNSARecord

        rec = DNSARecord(self.zone)
        rec.set_data(IPv4Address(u"192.168.0.1"))

        self.api.add_record(self.zone, rec)
        self.assertTrue(self.api.del_record(self.zone, rec))

    def test_delete_record_invalid(self):
        with self.assertRaises(TypeError) as context:
            self.api.del_record(self.zone, u"invalid")

    def test_delete_record_invalid2(self):
        from pypdnsrest.dnsrecords import DNSARecord
        rec = DNSARecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            self.api.del_record(self.zone, rec)
