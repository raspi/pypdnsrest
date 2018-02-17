from pypdnsrest.dnsrecords import DNSPtrRecord
from ipaddress import IPv4Address
from ipaddress import IPv6Address
from pypdnsrest.dnsrecords import InvalidDNSRecordException
from tests.records.test_records import TestRecords


class TestPtrRecord(TestRecords):
    def test_record_ipv4(self):
        rec = DNSPtrRecord(self.zone)
        self.assertTrue(rec.set_data(IPv4Address(u"127.0.0.1")))

    def test_record_ipv6(self):
        rec = DNSPtrRecord(self.zone)
        self.assertTrue(rec.set_data(IPv6Address(u"fd12:3456:789a:bcde:f012:3456:789a:bcde")))

    def test_record_empty(self):
        rec = DNSPtrRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data("")

    def test_record_empty2(self):
        rec = DNSPtrRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(None)

    def test_to_str(self):
        from ipaddress import IPv4Address
        rec = DNSPtrRecord(self.zone)
        rec.set_data(IPv4Address(u"127.0.0.1"))
        self.assertIsInstance(str(rec), str)

    def test_get_record(self):
        rec = DNSPtrRecord(self.zone)
        rec.set_data(IPv4Address(u"127.0.0.1"))
        self.assertIsInstance(rec.get_record(), dict)