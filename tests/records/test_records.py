"""
Test internal classes
"""

import unittest


class TestRecordMainBaseClass(unittest.TestCase):
    def test_set_data(self):
        from pypdnsrest.dnsrecords import DNSRecordMainBase
        c = DNSRecordMainBase()
        with self.assertRaises(NotImplementedError) as context:
            c.set_data()

    def test_validate(self):
        from pypdnsrest.dnsrecords import DNSRecordMainBase
        c = DNSRecordMainBase()
        with self.assertRaises(NotImplementedError) as context:
            c.validate()


class TestRecordBaseClass(unittest.TestCase):
    def test_set_data(self):
        from pypdnsrest.dnsrecords import DNSRecordBase
        c = DNSRecordBase(u"")
        with self.assertRaises(NotImplementedError) as context:
            c.set_data()

    def test_get_data(self):
        from pypdnsrest.dnsrecords import DNSRecordBase
        c = DNSRecordBase(u"")
        self.assertIsNone(c.get_data())

    def test_validate(self):
        from pypdnsrest.dnsrecords import DNSRecordBase
        c = DNSRecordBase(u"")
        with self.assertRaises(NotImplementedError) as context:
            c.validate()

    def test_str(self):
        from pypdnsrest.dnsrecords import DNSRecordBase
        self.assertIsInstance(str(DNSRecordBase(u"")), str)


class TestRecords(unittest.TestCase):
    def setUp(self):
        self.zone = u"{0}.zone.".format(type(self).__name__.lower())


