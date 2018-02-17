from pypdnsrest.dnsrecords import DNSNsRecord
from pypdnsrest.dnsrecords import InvalidDNSRecordException
from tests.records.test_records import TestRecords


class TestNsRecord(TestRecords):
    def test_record(self):
        rec = DNSNsRecord(self.zone)
        self.assertTrue(rec.set_data(u"test.test."))

    def test_record_empty(self):
        rec = DNSNsRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data("")

    def test_record_empty2(self):
        rec = DNSNsRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(None)

    def test_invalid_ipv4(self):
        rec = DNSNsRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(u"192.168.0.1")

    def test_invalid_ipv6(self):
        rec = DNSNsRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(u"fd12:3456:789a:bcde:f012:3456:789a:bcde")

    def test_invalid_type(self):
        rec = DNSNsRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(int(1))