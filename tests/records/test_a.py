from pypdnsrest.dnsrecords import DNSARecord
from ipaddress import IPv4Address
from pypdnsrest.dnsrecords import InvalidDNSRecordException
from tests.records.test_records import TestRecords


class TestARecord(TestRecords):
    def test_record(self):
        rec = DNSARecord(self.zone)
        self.assertTrue(rec.set_data(IPv4Address(u"192.168.0.1")))

    def test_record_empty(self):
        rec = DNSARecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data("")

    def test_record_empty2(self):
        rec = DNSARecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(None)

    def test_record_invalid(self):
        rec = DNSARecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(int(1))