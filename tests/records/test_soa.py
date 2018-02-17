from pypdnsrest.dnsrecords import DNSSoaRecordData
from pypdnsrest.dnsrecords import DNSSoaRecord
from pypdnsrest.dnsrecords import InvalidDNSRecordException
from datetime import timedelta
from tests.records.test_records import TestRecords


class TestSoaRecord(TestRecords):
    def test_record(self):
        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), 1)

        rec = DNSSoaRecord(self.zone)
        self.assertTrue(rec.set_data(soadata))

    def test_record2(self):
        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), 1, timedelta(hours=1),
                                   timedelta(hours=1), timedelta(hours=1), timedelta(hours=1))

        rec = DNSSoaRecord(self.zone)
        self.assertTrue(rec.set_data(soadata))

    def test_record_str(self):
        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), 1)

        rec = DNSSoaRecord(self.zone)
        rec.set_data(soadata)

        self.assertIsInstance(str(rec), str)

    def test_record_empty_nameserver(self):
        soadata = DNSSoaRecordData("", u"admin.{0}".format(self.zone), 1)

        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(soadata)

    def test_record_empty_nameserver2(self):
        soadata = DNSSoaRecordData(None, u"admin.{0}".format(self.zone), 1)

        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(soadata)

    def test_record_empty_admin(self):
        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"", 1)

        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(soadata)

    def test_record_empty_admin2(self):
        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), None, 1)

        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(soadata)

    def test_record_invalid_admin(self):
        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"test", 1)

        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(soadata)

    def test_record_wrong_serial(self):
        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), -1)

        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(soadata)

    def test_record_wrong_serial2(self):
        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), "invalid")

        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(soadata)

    def test_invalid_ttl(self):
        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), 1, timedelta(hours=1),
                                   timedelta(hours=1), timedelta(hours=1), timedelta(seconds=1))

        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(soadata)

    def test_record_data_none(self):
        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(None)

    def test_data_type_invalid(self):
        rec = DNSSoaRecord(self.zone)
        with self.assertRaises(InvalidDNSRecordException) as context:
            rec.set_data(u"invalid")