from pypdnsrest.dnsrecords import DNSCNameRecord
from pypdnsrest.dnsrecords import InvalidDNSRecordException
from tests.records.test_records import TestRecords


class TestCnameRecord(TestRecords):
    def test_record(self):
        rec = DNSCNameRecord(self.zone)
        self.assertTrue(rec.set_data(u"test.test."))

    def test_record_empty(self):
        rec = DNSCNameRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data("")

    def test_record_empty2(self):
        rec = DNSCNameRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(None)

    def test_invalid(self):
        rec = DNSCNameRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(int(1))