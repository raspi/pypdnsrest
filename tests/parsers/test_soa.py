from pypdnsrest.parsers import SoaRecordParser
from pypdnsrest.dnsrecords import DNSSoaRecord
from pypdnsrest.dnsrecords import DNSSoaRecordData

from tests.parsers.test_parsers import TestParserBase

class TestSoaParser(TestParserBase):
    def test_parser(self):
        p = SoaRecordParser()
        rec = p.parse(self.zone, u"ns1.{0} admin.{0} 1 3600 3600 3600 3600".format(self.zone), 3600)
        self.assertIsInstance(rec, DNSSoaRecord)

    def test_invalid_data(self):
        p = SoaRecordParser()

        with self.assertRaises(ValueError) as context:
            p.parse(self.zone, u"invalid data".format(self.zone), 3600)

    def test_data(self):
        expected = u"ns1.{0} admin.{0} 1 123 456 789 1011".format(self.zone)
        p = SoaRecordParser()
        rec = p.parse(self.zone, expected, 3600)
        self.assertIsInstance(rec, DNSSoaRecord)
        data = rec.get_record()['data']
        self.assertTrue(data == expected)
