from ipaddress import IPv6Address
from pypdnsrest.parsers import PtrRecordParser
from pypdnsrest.dnsrecords import DNSPtrRecord

from tests.parsers.test_parsers import TestParserBase


class TestPtrParser(TestParserBase):
    def test_parser_ipv4(self):
        p = PtrRecordParser()
        rec = p.parse(self.zone, u"1.0.168.192.in-addr.arpa.", 3600)
        self.assertIsInstance(rec, DNSPtrRecord)

    def test_parser_ipv6(self):
        p = PtrRecordParser()
        rec = p.parse(self.zone, u"e.d.c.b.a.9.8.7.6.5.4.3.2.1.0.f.e.d.c.b.a.9.8.7.6.5.4.3.2.1.d.f.ip6.arpa.", 3600)
        self.assertIsInstance(rec, DNSPtrRecord)

    def test_parser_ipv6_value(self):
        p = PtrRecordParser()
        parsedata = u"e.d.c.b.a.9.8.7.6.5.4.3.2.1.0.f.e.d.c.b.a.9.8.7.6.5.4.3.2.1.d.f.ip6.arpa"
        rec = p.parse(self.zone, parsedata, 3600)
        self.assertTrue(rec.get_data().reverse_pointer == parsedata)

    def test_parser_ipv6_value2(self):
        p = PtrRecordParser()

        parsedata = IPv6Address("fd00::")
        expected = u"0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.d.f.ip6.arpa"
        rec = p.parse(self.zone, parsedata.reverse_pointer, 3600)
        self.assertTrue(rec.get_data().reverse_pointer == expected)

    def test_parser_empty(self):
        p = PtrRecordParser()
        with self.assertRaises(ValueError) as context:
            p.parse(self.zone, u"", 3600)

    def test_parser_empty2(self):
        p = PtrRecordParser()
        with self.assertRaises(AttributeError) as context:
            p.parse(self.zone, None, 3600)

    def test_parser_invalid(self):
        p = PtrRecordParser()
        with self.assertRaises(ValueError) as context:
            p.parse(self.zone, u"invalid", 3600)

    def test_parser_invalid2(self):
        p = PtrRecordParser()
        with self.assertRaises(ValueError) as context:
            p.parse(self.zone, u"1.2.3.in-addr.arpa.", 3600)