import unittest

from pypdnsrest.client import PowerDnsRestApiClient
from pypdnsrest.parsers import RecordParser


class SoaRecordParser(RecordParser):
    """
    Broken parser
    """

    def parse(self, name: str, data: str, ttl: int):
        raise ValueError("Invalid value: '{0}'".format(data))


class TestApiParsers(unittest.TestCase):
    def setUp(self):
        self.api = PowerDnsRestApiClient(u"pdnsapi")
        self.zone = u"{0}.zone.".format(type(self).__name__.lower())
        self.nameservers = [
            u"ns1.{0}".format(self.zone),
            u"ns2.{0}".format(self.zone)
        ]

        try:
            # It's possible that failed test left old zone remains
            self.api.del_zone(self.zone)
        except Exception:
            pass

    def tearDown(self):
        try:
            self.api.del_zone(self.zone)
        except Exception:
            pass

    def test_parser(self):
        from pypdnsrest.parsers import ARecordParser
        self.assertTrue(self.api.add_parser(ARecordParser()))

    def test_parser2(self):
        from pypdnsrest.parsers import ARecordParser
        self.api.add_parser(ARecordParser())
        self.assertTrue(self.api.add_parser(ARecordParser()))

    def test_parser_invalid(self):
        with self.assertRaises(TypeError) as context:
            self.api.add_parser(int(1))

    def test_parser_invalid2(self):
        self.api.add_parser(SoaRecordParser())
        self.api.add_zone(self.zone, self.nameservers)

        with self.assertRaises(ValueError) as context:
            self.api.get_zone(self.zone)
