"""
Test internal classes
"""

import unittest

from pypdnsrest.dnsrecords import InvalidDNSRecordException


class TestRecords(unittest.TestCase):
    def setUp(self):
        self.zone = u"{0}.zone.".format(type(self).__name__.lower())


class TestARecord(TestRecords):
    def test_record(self):
        from pypdnsrest.dnsrecords import DNSARecord
        from ipaddress import IPv4Address
        rec = DNSARecord(self.zone)
        self.assertTrue(rec.set_data(IPv4Address(u"192.168.0.1")))

    def test_record_empty(self):
        from pypdnsrest.dnsrecords import DNSARecord
        rec = DNSARecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data("")

    def test_record_empty2(self):
        from pypdnsrest.dnsrecords import DNSARecord
        rec = DNSARecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(None)


class TestAaaaRecord(TestRecords):
    def test_record(self):
        from pypdnsrest.dnsrecords import DNSAaaaRecord
        from ipaddress import IPv6Address
        rec = DNSAaaaRecord(self.zone)
        self.assertTrue(rec.set_data(IPv6Address(u"fd00::")))

    def test_record_empty(self):
        from pypdnsrest.dnsrecords import DNSAaaaRecord
        rec = DNSAaaaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(u"")

    def test_record_empty2(self):
        from pypdnsrest.dnsrecords import DNSAaaaRecord
        rec = DNSAaaaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(None)


class TestCnameRecord(TestRecords):
    def test_record(self):
        from pypdnsrest.dnsrecords import DNSCNameRecord
        rec = DNSCNameRecord(self.zone)
        self.assertTrue(rec.set_data(u"test.test."))

    def test_record_empty(self):
        from pypdnsrest.dnsrecords import DNSCNameRecord
        rec = DNSCNameRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data("")

    def test_record_empty2(self):
        from pypdnsrest.dnsrecords import DNSCNameRecord
        rec = DNSCNameRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(None)


class TestNsRecord(TestRecords):
    def test_record(self):
        from pypdnsrest.dnsrecords import DNSNsRecord
        rec = DNSNsRecord(self.zone)
        self.assertTrue(rec.set_data(u"test.test."))

    def test_record_empty(self):
        from pypdnsrest.dnsrecords import DNSNsRecord
        rec = DNSNsRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data("")

    def test_record_empty2(self):
        from pypdnsrest.dnsrecords import DNSNsRecord
        rec = DNSNsRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(None)


class TestMxRecord(TestRecords):
    def test_record(self):
        from pypdnsrest.dnsrecords import DNSMxRecord
        from pypdnsrest.dnsrecords import DNSMxRecordData

        mxdata = DNSMxRecordData(u"mail.{0}".format(self.zone), 10)

        rec = DNSMxRecord(self.zone)
        self.assertTrue(rec.set_data(mxdata))

    def test_record_wrong_priority(self):
        from pypdnsrest.dnsrecords import DNSMxRecord
        from pypdnsrest.dnsrecords import DNSMxRecordData

        mxdata = DNSMxRecordData(u"mail.{0}".format(self.zone), -1)

        rec = DNSMxRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(mxdata)


class TestSoaRecord(TestRecords):
    def test_record(self):
        from pypdnsrest.dnsrecords import DNSSoaRecordData
        from pypdnsrest.dnsrecords import DNSSoaRecord

        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), 1)

        rec = DNSSoaRecord(self.zone)
        self.assertTrue(rec.set_data(soadata))

    def test_record_empty_nameserver(self):
        from pypdnsrest.dnsrecords import DNSSoaRecordData
        from pypdnsrest.dnsrecords import DNSSoaRecord

        soadata = DNSSoaRecordData("", u"admin.{0}".format(self.zone), 1)

        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(soadata)

    def test_record_empty_nameserver2(self):
        from pypdnsrest.dnsrecords import DNSSoaRecordData
        from pypdnsrest.dnsrecords import DNSSoaRecord

        soadata = DNSSoaRecordData(None, u"admin.{0}".format(self.zone), 1)

        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(soadata)

    def test_record_empty_admin(self):
        from pypdnsrest.dnsrecords import DNSSoaRecordData
        from pypdnsrest.dnsrecords import DNSSoaRecord

        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"", 1)

        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(soadata)

    def test_record_empty_admin2(self):
        from pypdnsrest.dnsrecords import DNSSoaRecordData
        from pypdnsrest.dnsrecords import DNSSoaRecord

        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), None, 1)

        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(soadata)

    def test_record_invalid_admin(self):
        from pypdnsrest.dnsrecords import DNSSoaRecordData
        from pypdnsrest.dnsrecords import DNSSoaRecord

        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"test", 1)

        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(soadata)

    def test_record_wrong_serial(self):
        from pypdnsrest.dnsrecords import DNSSoaRecordData
        from pypdnsrest.dnsrecords import DNSSoaRecord

        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), -1)

        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(soadata)


class TestPtrRecord(TestRecords):
    def test_record_ipv4(self):
        from pypdnsrest.dnsrecords import DNSPtrRecord
        from ipaddress import IPv4Address
        rec = DNSPtrRecord(self.zone)
        self.assertTrue(rec.set_data(IPv4Address(u"127.0.0.1")))

    def test_record_ipv6(self):
        from pypdnsrest.dnsrecords import DNSPtrRecord
        from ipaddress import IPv6Address
        rec = DNSPtrRecord(self.zone)
        self.assertTrue(rec.set_data(IPv6Address(u"fd00::")))

    def test_record_empty(self):
        from pypdnsrest.dnsrecords import DNSPtrRecord
        rec = DNSPtrRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data("")

    def test_record_empty2(self):
        from pypdnsrest.dnsrecords import DNSPtrRecord
        rec = DNSPtrRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(None)
