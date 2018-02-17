from pypdnsrest.dnsrecords import DNSTxtRecord
from pypdnsrest.dnsrecords import InvalidDNSRecordException
from tests.records.test_records import TestRecords


class TestTxtRecord(TestRecords):
    def test_record(self):
        rec = DNSTxtRecord(self.zone)
        self.assertTrue(rec.set_data(u"test text data"))

    def test_none(self):
        rec = DNSTxtRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(None)

    def test_empty(self):
        rec = DNSTxtRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(u"")

    def test_invalid(self):
        rec = DNSTxtRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(int(1))