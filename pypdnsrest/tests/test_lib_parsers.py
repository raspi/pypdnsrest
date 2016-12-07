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

    def test_parser_empty(self):
        from pypdnsrest.parsers import PtrRecordParser
        p = PtrRecordParser()
        with self.assertRaises(ValueError) as context:
            rec = p.parse(self.zone, u"", 3600)

    def test_parser_empty2(self):
        from pypdnsrest.parsers import PtrRecordParser
        p = PtrRecordParser()
        with self.assertRaises(AttributeError) as context:
            rec = p.parse(self.zone, None, 3600)
