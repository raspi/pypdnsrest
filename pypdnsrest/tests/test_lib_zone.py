"""
Test internal classes
"""

import unittest

from pypdnsrest.dnszone import DNSZone


class TestZone(unittest.TestCase):
    def setUp(self):
        self.zone = "{0}.zone.".format(type(self).__name__.lower())

    def test_add_a_record(self):
        from pypdnsrest.dnsrecords import DNSARecord
        from ipaddress import IPv4Address

        z = DNSZone()

        rec = DNSARecord(self.zone)
        rec.set_data(IPv4Address("192.168.0.1"))
        self.assertTrue(z.add_record(rec))

    def test_add_aaaa_record(self):
        from pypdnsrest.dnsrecords import DNSAaaaRecord
        from ipaddress import IPv6Address

        z = DNSZone()

        rec = DNSAaaaRecord(self.zone)
        rec.set_data(IPv6Address("fd00::"))
        self.assertTrue(z.add_record(rec))

    def test_add_cname_record(self):
        from pypdnsrest.dnsrecords import DNSCNameRecord

        z = DNSZone()

        rec = DNSCNameRecord(self.zone)
        rec.set_data("test.test.")
        self.assertTrue(z.add_record(rec))

    def test_add_ns_record(self):
        from pypdnsrest.dnsrecords import DNSNsRecord

        z = DNSZone()

        rec = DNSNsRecord(self.zone)
        rec.set_data("ns1.{0}".format(self.zone))
        self.assertTrue(z.add_record(rec))

    def test_add_soa_record(self):
        from pypdnsrest.dnsrecords import DNSSoaRecord
        from pypdnsrest.dnsrecords import DNSSoaRecordData

        soadata = DNSSoaRecordData("ns1.{0}".format(self.zone), "admin.{0}".format(self.zone), 1)

        rec = DNSSoaRecord(self.zone)
        rec.set_data(soadata)

        z = DNSZone()
        self.assertTrue(z.add_record(rec))

    def test_add_mx_record(self):
        from pypdnsrest.dnsrecords import DNSMxRecord
        from pypdnsrest.dnsrecords import DNSMxRecordData

        mxdata = DNSMxRecordData("mail.{0}".format(self.zone), 10)

        rec = DNSMxRecord(self.zone)
        rec.set_data(mxdata)

        z = DNSZone()
        self.assertTrue(z.add_record(rec))

    def test_add_ptr_record(self):
        from pypdnsrest.dnsrecords import DNSPtrRecord
        from ipaddress import IPv4Address

        rec = DNSPtrRecord(self.zone)
        rec.set_data(IPv4Address("192.168.0.1"))

        z = DNSZone()
        self.assertTrue(z.add_record(rec))

    def test_empty(self):
        z = DNSZone()
        self.assertFalse(z.validate())

    def test_valid(self):
        z = DNSZone()

        from pypdnsrest.dnsrecords import DNSNsRecord
        rec = DNSNsRecord(self.zone)
        rec.set_data("ns1.{0}".format(self.zone))
        z.add_record(rec)

        from pypdnsrest.dnsrecords import DNSARecord
        from ipaddress import IPv4Address
        z.add_record(rec)

        rec = DNSARecord(self.zone)
        rec.set_data(IPv4Address("192.168.0.1"))

        self.assertTrue(z.validate())
