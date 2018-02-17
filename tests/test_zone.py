"""
Test internal classes
"""

import unittest

from pypdnsrest.dnsrecords import InvalidDNSRecordException
from pypdnsrest.dnszone import DNSZone


class TestZone(unittest.TestCase):
    def setUp(self):
        self.zone = u"{0}-unittest.zone.".format(type(self).__name__.lower())

    def test_add_a_record(self):
        from pypdnsrest.dnsrecords import DNSARecord
        from ipaddress import IPv4Address

        z = DNSZone()

        rec = DNSARecord(self.zone)
        rec.set_data(IPv4Address(u"192.168.0.1"))
        self.assertTrue(z.add_record(rec))

    def test_add_aaaa_record(self):
        from pypdnsrest.dnsrecords import DNSAaaaRecord
        from ipaddress import IPv6Address

        z = DNSZone()

        rec = DNSAaaaRecord(self.zone)
        rec.set_data(IPv6Address(u"fd12:3456:789a:bcde:f012:3456:789a:bcde"))
        self.assertTrue(z.add_record(rec))

    def test_add_cname_record(self):
        from pypdnsrest.dnsrecords import DNSCNameRecord

        z = DNSZone()

        rec = DNSCNameRecord(self.zone)
        rec.set_data(u"test.test.")
        self.assertTrue(z.add_record(rec))

    def test_add_ns_record(self):
        from pypdnsrest.dnsrecords import DNSNsRecord

        z = DNSZone()

        rec = DNSNsRecord(self.zone)
        rec.set_data(u"ns1.{0}".format(self.zone))
        self.assertTrue(z.add_record(rec))

    def test_add_soa_record(self):
        from pypdnsrest.dnsrecords import DNSSoaRecord
        from pypdnsrest.dnsrecords import DNSSoaRecordData

        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), 1)

        rec = DNSSoaRecord(self.zone)
        rec.set_data(soadata)

        z = DNSZone()
        self.assertTrue(z.add_record(rec))

    def test_add_mx_record(self):
        from pypdnsrest.dnsrecords import DNSMxRecord
        from pypdnsrest.dnsrecords import DNSMxRecordData

        mxdata = DNSMxRecordData(u"mail.{0}".format(self.zone), 10)

        rec = DNSMxRecord(self.zone)
        rec.set_data(mxdata)

        z = DNSZone()
        self.assertTrue(z.add_record(rec))

    def test_add_ptr_record(self):
        from pypdnsrest.dnsrecords import DNSPtrRecord
        from ipaddress import IPv4Address

        rec = DNSPtrRecord(self.zone)
        rec.set_data(IPv4Address(u"192.168.0.1"))

        z = DNSZone()
        self.assertTrue(z.add_record(rec))

    def test_empty(self):
        z = DNSZone()
        self.assertFalse(z.validate())

    def test_valid(self):
        z = DNSZone()

        # Add SOA
        from pypdnsrest.dnsrecords import DNSSoaRecordData
        from pypdnsrest.dnsrecords import DNSSoaRecord

        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), 1)
        rec = DNSSoaRecord(self.zone)
        rec.set_data(soadata)
        z.add_record(rec)

        # Add NS
        from pypdnsrest.dnsrecords import DNSNsRecord
        rec = DNSNsRecord(self.zone)
        rec.set_data(u"ns1.{0}".format(self.zone))
        z.add_record(rec)

        rec = DNSNsRecord(self.zone)
        rec.set_data(u"ns2.{0}".format(self.zone))
        z.add_record(rec)

        # Add A
        from pypdnsrest.dnsrecords import DNSARecord
        from ipaddress import IPv4Address

        rec = DNSARecord(self.zone)
        rec.set_data(IPv4Address(u"192.168.0.1"))
        z.add_record(rec)

        self.assertTrue(z.validate())

    def test_invalid_type(self):
        z = DNSZone()
        with self.assertRaises(InvalidDNSRecordException) as context:
            z.add_record(int(1))

    def test_invalid_data(self):
        from pypdnsrest.dnsrecords import DNSNsRecord

        z = DNSZone()
        rec = DNSNsRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            z.add_record(rec)

    def test_to_string(self):
        from pypdnsrest.dnsrecords import DNSSoaRecord
        from pypdnsrest.dnsrecords import DNSSoaRecordData

        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), 1)

        rec = DNSSoaRecord(self.zone)
        rec.set_data(soadata)

        z = DNSZone()
        z.add_record(rec)

        self.assertIsInstance(str(z), str)

    def test_invalid_zone(self):
        from pypdnsrest.dnsrecords import DNSSoaRecord
        from pypdnsrest.dnsrecords import DNSSoaRecordData

        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), 1)

        rec = DNSSoaRecord(self.zone)
        rec.set_data(soadata)

        z = DNSZone()
        z.add_record(rec)

        self.assertFalse(z.validate())
