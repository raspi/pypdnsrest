# -*- coding: utf8 -*-

from pypdnsrest.dnsrecords import DNSNsRecord
from pypdnsrest.dnsrecords import DNSRecordMainBase
from pypdnsrest.dnsrecords import DNSSoaRecord
from pypdnsrest.dnsrecords import InvalidDNSRecordException


class DNSZoneException(Exception):
    pass


class DNSZoneInvalidException(DNSZoneException):
    pass


class DNSZoneBase:
    pass


class DNSZone(DNSZoneBase):
    records = []

    def add_record(self, record: DNSRecordMainBase):

        if not isinstance(record, DNSRecordMainBase):
            raise InvalidDNSRecordException()

        if record.validate():
            self.records.append(record)
        else:
            raise InvalidDNSRecordException("Invalid record")

    def get_records(self):
        return self.records

    def validate(self):
        if len(self.records) == 0:
            return False

        has_soa = False
        nameserver_count = 0

        for rec in self.get_records():
            if isinstance(rec, DNSSoaRecord):
                has_soa = True
            elif isinstance(rec, DNSNsRecord):
                nameserver_count += 1

        if has_soa and nameserver_count >= 1:
            return True

        return False

    def __str__(self):
        for i in self.get_records():
            return "{0}".format(i)
