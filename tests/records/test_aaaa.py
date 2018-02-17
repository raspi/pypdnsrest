from pypdnsrest.dnsrecords import InvalidDNSRecordException
from tests.records.test_records import TestRecords
from pypdnsrest.dnsrecords import DNSAaaaRecord
from ipaddress import IPv6Address


class TestAaaaRecord(TestRecords):
    def test_record(self):
        rec = DNSAaaaRecord(self.zone)
        self.assertTrue(rec.set_data(IPv6Address(u"fd12:3456:789a:bcde:f012:3456:789a:bcde")))

    def test_record_empty(self):
        rec = DNSAaaaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(u"")

    def test_record_empty2(self):
        rec = DNSAaaaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(None)