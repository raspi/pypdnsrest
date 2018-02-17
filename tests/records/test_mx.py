from pypdnsrest.dnsrecords import DNSMxRecord
from pypdnsrest.dnsrecords import DNSMxRecordData
from pypdnsrest.dnsrecords import InvalidDNSRecordException
from datetime import timedelta
from tests.records.test_records import TestRecords


class TestMxRecord(TestRecords):
    def test_record(self):
        mxdata = DNSMxRecordData(u"mail.{0}".format(self.zone), 10)

        rec = DNSMxRecord(self.zone)
        self.assertTrue(rec.set_data(mxdata))

    def test_record2(self):
        mxdata = DNSMxRecordData(u"mail.{0}".format(self.zone), 10, timedelta(hours=1))

        rec = DNSMxRecord(self.zone)
        self.assertTrue(rec.set_data(mxdata))

    def test_record_wrong_priority(self):
        mxdata = DNSMxRecordData(u"mail.{0}".format(self.zone), -1)

        rec = DNSMxRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(mxdata)

    def test_invalid_server_type(self):
        mxdata = DNSMxRecordData(int(1), 10)

        rec = DNSMxRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(mxdata)

    def test_invalid_server(self):
        mxdata = DNSMxRecordData(u"invalid", 10)

        rec = DNSMxRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(mxdata)

    def test_invalid_priority_type(self):
        mxdata = DNSMxRecordData(u"mail.{0}".format(self.zone), u"invalid")

        rec = DNSMxRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(mxdata)

    def test_data_none(self):
        rec = DNSMxRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(None)

    def test_data_invalid(self):
        rec = DNSMxRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(u"invalid")