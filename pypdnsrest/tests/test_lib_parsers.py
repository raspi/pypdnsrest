"""
Test internal classes
"""

import unittest

from pypdnsrest.dnsrecords import InvalidDNSRecordException


class TestParserBase(unittest.TestCase):
    def setUp(self):
        self.zone = u"{0}.zone.".format(type(self).__name__.lower())


class TestParserBaseClass(TestParserBase):
    def test_class(self):
        from pypdnsrest.parsers import RecordParser
        p = RecordParser()
        with self.assertRaises(NotImplementedError) as context:
            p.parse("", [], 0)


class TestAParser(TestParserBase):
    def test_parser(self):
        from pypdnsrest.parsers import ARecordParser
        from pypdnsrest.dnsrecords import DNSARecord
        p = ARecordParser()
        rec = p.parse(self.zone, u"192.168.0.1", 3600)
        self.assertIsInstance(rec, DNSARecord)

    def test_empty(self):
        from pypdnsrest.parsers import ARecordParser
        from ipaddress import AddressValueError
        p = ARecordParser()
        with self.assertRaises(AddressValueError) as context:
            p.parse(self.zone, u"", 3600)

    def test_empty2(self):
        from pypdnsrest.parsers import ARecordParser
        from ipaddress import AddressValueError
        p = ARecordParser()
        with self.assertRaises(AddressValueError) as context:
            p.parse(self.zone, None, 3600)

    def test_invalid(self):
        from pypdnsrest.parsers import ARecordParser
        from ipaddress import AddressValueError
        p = ARecordParser()
        with self.assertRaises(AddressValueError) as context:
            p.parse(self.zone, u"invalid", 3600)


class TestAaaaParser(TestParserBase):
    def test_parser(self):
        from pypdnsrest.parsers import AaaaRecordParser
        from pypdnsrest.dnsrecords import DNSAaaaRecord
        p = AaaaRecordParser()
        rec = p.parse(self.zone, u"fd12:3456:789a:bcde:f012:3456:789a:bcde", 3600)
        self.assertIsInstance(rec, DNSAaaaRecord)


class TestNsParser(TestParserBase):
    def test_parser(self):
        from pypdnsrest.parsers import NsRecordParser
        from pypdnsrest.dnsrecords import DNSNsRecord
        p = NsRecordParser()
        rec = p.parse(self.zone, u"ns1.{0}".format(self.zone), 3600)
        self.assertIsInstance(rec, DNSNsRecord)

    def test_empty(self):
        from pypdnsrest.parsers import NsRecordParser
        p = NsRecordParser()
        with self.assertRaises(InvalidDNSRecordException) as context:
            p.parse(self.zone, u"", 3600)

    def test_empty2(self):
        from pypdnsrest.parsers import NsRecordParser
        p = NsRecordParser()
        with self.assertRaises(InvalidDNSRecordException) as context:
            p.parse(self.zone, None, 3600)

    def test_invalid_ipv6(self):
        from pypdnsrest.parsers import NsRecordParser
        p = NsRecordParser()
        with self.assertRaises(InvalidDNSRecordException) as context:
            p.parse(self.zone, u"fd12:3456:789a:bcde:f012:3456:789a:bcde", 3600)


class TestPtrParser(TestParserBase):
    def test_parser_ipv4(self):
        from pypdnsrest.parsers import PtrRecordParser
        from pypdnsrest.dnsrecords import DNSPtrRecord
        p = PtrRecordParser()
        rec = p.parse(self.zone, u"1.0.168.192.in-addr.arpa.", 3600)
        self.assertIsInstance(rec, DNSPtrRecord)

    def test_parser_ipv6(self):
        from pypdnsrest.parsers import PtrRecordParser
        from pypdnsrest.dnsrecords import DNSPtrRecord
        p = PtrRecordParser()
        rec = p.parse(self.zone, u"e.d.c.b.a.9.8.7.6.5.4.3.2.1.0.f.e.d.c.b.a.9.8.7.6.5.4.3.2.1.d.f.ip6.arpa.", 3600)
        self.assertIsInstance(rec, DNSPtrRecord)

    def test_parser_ipv6_value(self):
        from pypdnsrest.parsers import PtrRecordParser
        p = PtrRecordParser()

        parsedata = u"e.d.c.b.a.9.8.7.6.5.4.3.2.1.0.f.e.d.c.b.a.9.8.7.6.5.4.3.2.1.d.f.ip6.arpa"
        rec = p.parse(self.zone, parsedata, 3600)
        self.assertTrue(rec.get_data().reverse_pointer == parsedata)

    def test_parser_ipv6_value2(self):
        from ipaddress import IPv6Address
        from pypdnsrest.parsers import PtrRecordParser
        p = PtrRecordParser()

        parsedata = IPv6Address("fd00::")
        expected = u"0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.d.f.ip6.arpa"
        rec = p.parse(self.zone, parsedata.reverse_pointer, 3600)
        self.assertTrue(rec.get_data().reverse_pointer == expected)

    def test_parser_empty(self):
        from pypdnsrest.parsers import PtrRecordParser
        p = PtrRecordParser()
        with self.assertRaises(ValueError) as context:
            p.parse(self.zone, u"", 3600)

    def test_parser_empty2(self):
        from pypdnsrest.parsers import PtrRecordParser
        p = PtrRecordParser()
        with self.assertRaises(AttributeError) as context:
            p.parse(self.zone, None, 3600)

    def test_parser_invalid(self):
        from pypdnsrest.parsers import PtrRecordParser
        p = PtrRecordParser()
        with self.assertRaises(ValueError) as context:
            p.parse(self.zone, u"invalid", 3600)

    def test_parser_invalid2(self):
        from pypdnsrest.parsers import PtrRecordParser
        p = PtrRecordParser()
        with self.assertRaises(ValueError) as context:
            p.parse(self.zone, u"1.2.3.in-addr.arpa.", 3600)


class TestSoaParser(TestParserBase):
    def test_parser(self):
        from pypdnsrest.parsers import SoaRecordParser
        from pypdnsrest.dnsrecords import DNSSoaRecord
        p = SoaRecordParser()
        rec = p.parse(self.zone, u"ns1.{0} admin.{0} 1 3600 3600 3600 3600".format(self.zone), 3600)
        self.assertIsInstance(rec, DNSSoaRecord)

    def test_invalid_data(self):
        from pypdnsrest.parsers import SoaRecordParser
        p = SoaRecordParser()

        with self.assertRaises(ValueError) as context:
            p.parse(self.zone, u"invalid data".format(self.zone), 3600)


class TestMxParser(TestParserBase):
    def test_parser(self):
        from pypdnsrest.parsers import MxRecordParser
        from pypdnsrest.dnsrecords import DNSMxRecord
        p = MxRecordParser()
        rec = p.parse(self.zone, u"10 mail.{0}".format(self.zone), 3600)
        self.assertIsInstance(rec, DNSMxRecord)


class TestCNameParser(TestParserBase):
    def test_parser(self):
        from pypdnsrest.parsers import CnameRecordParser
        from pypdnsrest.dnsrecords import DNSCNameRecord
        p = CnameRecordParser()
        rec = p.parse(self.zone, u"alias.{0}".format(self.zone), 3600)
        self.assertIsInstance(rec, DNSCNameRecord)


class TestTxtParser(TestParserBase):
    def test_parser(self):
        from pypdnsrest.parsers import TxtRecordParser
        from pypdnsrest.dnsrecords import DNSTxtRecord
        p = TxtRecordParser()
        rec = p.parse(self.zone, u"test", 3600)
        self.assertIsInstance(rec, DNSTxtRecord)
