"""
Test internal classes
"""

import unittest

from pypdnsrest.dnsrecords import InvalidDNSRecordException


class TestRecordMainBaseClass(unittest.TestCase):
    def test_set_data(self):
        from pypdnsrest.dnsrecords import DNSRecordMainBase
        c = DNSRecordMainBase()
        with self.assertRaises(NotImplementedError) as context:
            c.set_data()

    def test_validate(self):
        from pypdnsrest.dnsrecords import DNSRecordMainBase
        c = DNSRecordMainBase()
        with self.assertRaises(NotImplementedError) as context:
            c.validate()


class TestRecordBaseClass(unittest.TestCase):
    def test_set_data(self):
        from pypdnsrest.dnsrecords import DNSRecordBase
        c = DNSRecordBase(u"")
        with self.assertRaises(NotImplementedError) as context:
            c.set_data()

    def test_get_data(self):
        from pypdnsrest.dnsrecords import DNSRecordBase
        c = DNSRecordBase(u"")
        self.assertIsNone(c.get_data())

    def test_validate(self):
        from pypdnsrest.dnsrecords import DNSRecordBase
        c = DNSRecordBase(u"")
        with self.assertRaises(NotImplementedError) as context:
            c.validate()

    def test_str(self):
        from pypdnsrest.dnsrecords import DNSRecordBase
        self.assertIsInstance(str(DNSRecordBase(u"")), str)


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

    def test_record_invalid(self):
        from pypdnsrest.dnsrecords import DNSARecord
        rec = DNSARecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(int(1))


class TestAaaaRecord(TestRecords):
    def test_record(self):
        from pypdnsrest.dnsrecords import DNSAaaaRecord
        from ipaddress import IPv6Address
        rec = DNSAaaaRecord(self.zone)
        self.assertTrue(rec.set_data(IPv6Address(u"fd12:3456:789a:bcde:f012:3456:789a:bcde")))

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

    def test_invalid(self):
        from pypdnsrest.dnsrecords import DNSCNameRecord
        rec = DNSCNameRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(int(1))


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

    def test_invalid_ipv4(self):
        from pypdnsrest.dnsrecords import DNSNsRecord
        rec = DNSNsRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(u"192.168.0.1")

    def test_invalid_ipv6(self):
        from pypdnsrest.dnsrecords import DNSNsRecord
        rec = DNSNsRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(u"fd12:3456:789a:bcde:f012:3456:789a:bcde")

    def test_invalid_type(self):
        from pypdnsrest.dnsrecords import DNSNsRecord
        rec = DNSNsRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(int(1))


class TestMxRecord(TestRecords):
    def test_record(self):
        from pypdnsrest.dnsrecords import DNSMxRecord
        from pypdnsrest.dnsrecords import DNSMxRecordData

        mxdata = DNSMxRecordData(u"mail.{0}".format(self.zone), 10)

        rec = DNSMxRecord(self.zone)
        self.assertTrue(rec.set_data(mxdata))

    def test_record2(self):
        from datetime import timedelta
        from pypdnsrest.dnsrecords import DNSMxRecord
        from pypdnsrest.dnsrecords import DNSMxRecordData

        mxdata = DNSMxRecordData(u"mail.{0}".format(self.zone), 10, timedelta(hours=1))

        rec = DNSMxRecord(self.zone)
        self.assertTrue(rec.set_data(mxdata))

    def test_record_wrong_priority(self):
        from pypdnsrest.dnsrecords import DNSMxRecord
        from pypdnsrest.dnsrecords import DNSMxRecordData

        mxdata = DNSMxRecordData(u"mail.{0}".format(self.zone), -1)

        rec = DNSMxRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(mxdata)

    def test_invalid_server_type(self):
        from pypdnsrest.dnsrecords import DNSMxRecord
        from pypdnsrest.dnsrecords import DNSMxRecordData

        mxdata = DNSMxRecordData(int(1), 10)

        rec = DNSMxRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(mxdata)

    def test_invalid_server(self):
        from pypdnsrest.dnsrecords import DNSMxRecord
        from pypdnsrest.dnsrecords import DNSMxRecordData

        mxdata = DNSMxRecordData(u"invalid", 10)

        rec = DNSMxRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(mxdata)

    def test_invalid_priority_type(self):
        from pypdnsrest.dnsrecords import DNSMxRecord
        from pypdnsrest.dnsrecords import DNSMxRecordData

        mxdata = DNSMxRecordData(u"mail.{0}".format(self.zone), u"invalid")

        rec = DNSMxRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(mxdata)

    def test_data_none(self):
        from pypdnsrest.dnsrecords import DNSMxRecord
        rec = DNSMxRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(None)

    def test_data_invalid(self):
        from pypdnsrest.dnsrecords import DNSMxRecord
        rec = DNSMxRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(u"invalid")


class TestSoaRecordData(TestRecords):
    def test_get_data(self):
        from pypdnsrest.dnsrecords import DNSSoaRecordData
        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), 1)
        self.assertIsInstance(soadata.get_data(), dict)

    def test_data_to_str(self):
        from pypdnsrest.dnsrecords import DNSSoaRecordData

        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), 1)
        self.assertIsInstance(str(soadata), str)


class TestSoaRecord(TestRecords):
    def test_record(self):
        from pypdnsrest.dnsrecords import DNSSoaRecordData
        from pypdnsrest.dnsrecords import DNSSoaRecord

        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), 1)

        rec = DNSSoaRecord(self.zone)
        self.assertTrue(rec.set_data(soadata))

    def test_record2(self):
        from datetime import timedelta
        from pypdnsrest.dnsrecords import DNSSoaRecordData
        from pypdnsrest.dnsrecords import DNSSoaRecord

        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), 1, timedelta(hours=1),
                                   timedelta(hours=1), timedelta(hours=1), timedelta(hours=1))

        rec = DNSSoaRecord(self.zone)
        self.assertTrue(rec.set_data(soadata))

    def test_record_str(self):
        from pypdnsrest.dnsrecords import DNSSoaRecordData
        from pypdnsrest.dnsrecords import DNSSoaRecord

        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), 1)

        rec = DNSSoaRecord(self.zone)
        rec.set_data(soadata)

        self.assertIsInstance(str(rec), str)

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

    def test_record_wrong_serial2(self):
        from pypdnsrest.dnsrecords import DNSSoaRecordData
        from pypdnsrest.dnsrecords import DNSSoaRecord

        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), "invalid")

        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(soadata)

    def test_invalid_ttl(self):
        from datetime import timedelta
        from pypdnsrest.dnsrecords import DNSSoaRecordData
        from pypdnsrest.dnsrecords import DNSSoaRecord

        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), 1, timedelta(hours=1),
                                   timedelta(hours=1), timedelta(hours=1), timedelta(seconds=1))

        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(soadata)

    def test_record_data_none(self):
        from pypdnsrest.dnsrecords import DNSSoaRecord

        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(None)

    def test_data_type_invalid(self):
        from pypdnsrest.dnsrecords import DNSSoaRecord

        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(u"invalid")


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
        self.assertTrue(rec.set_data(IPv6Address(u"fd12:3456:789a:bcde:f012:3456:789a:bcde")))

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

    def test_to_str(self):
        from pypdnsrest.dnsrecords import DNSPtrRecord
        from ipaddress import IPv4Address
        rec = DNSPtrRecord(self.zone)
        rec.set_data(IPv4Address(u"127.0.0.1"))
        self.assertIsInstance(str(rec), str)

    def test_get_record(self):
        from pypdnsrest.dnsrecords import DNSPtrRecord
        from ipaddress import IPv4Address
        rec = DNSPtrRecord(self.zone)
        rec.set_data(IPv4Address(u"127.0.0.1"))
        self.assertIsInstance(rec.get_record(), dict)


class TestTxtRecord(TestRecords):
    def test_record(self):
        from pypdnsrest.dnsrecords import DNSTxtRecord
        rec = DNSTxtRecord(self.zone)
        self.assertTrue(rec.set_data(u"test text data"))

    def test_none(self):
        from pypdnsrest.dnsrecords import DNSTxtRecord
        rec = DNSTxtRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(None)

    def test_empty(self):
        from pypdnsrest.dnsrecords import DNSTxtRecord
        rec = DNSTxtRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(u"")

    def test_invalid(self):
        from pypdnsrest.dnsrecords import DNSTxtRecord
        rec = DNSTxtRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(int(1))
