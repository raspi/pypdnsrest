from pypdnsrest.dnsrecords import DNSSoaRecordData

from tests.records.test_records import TestRecords


class TestSoaRecordData(TestRecords):
    def test_get_data(self):
        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), 1)
        self.assertIsInstance(soadata.get_data(), dict)

    def test_data_to_str(self):
        soadata = DNSSoaRecordData(u"ns1.{0}".format(self.zone), u"admin.{0}".format(self.zone), 1)
        self.assertIsInstance(str(soadata), str)