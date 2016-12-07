# -*- coding: utf8 -*-
import logging

log = logging.getLogger(__name__)

from pypdnsrest.dnsrecords import DNSNsRecord
from pypdnsrest.dnsrecords import DNSRecordMainBase
from pypdnsrest.dnsrecords import DNSSoaRecord
from pypdnsrest.dnsrecords import InvalidDNSRecordException


class DNSZoneException(Exception):
    pass


class DNSZoneInvalidException(DNSZoneException):
    pass


class DNSZoneBase():
    _records = []

    def __init__(self):
        self._records = []

    def get_records(self) -> list:
        return self._records


class DNSZone(DNSZoneBase):
    def add_record(self, record: DNSRecordMainBase) -> bool:

        if not isinstance(record, DNSRecordMainBase):
            raise InvalidDNSRecordException(u"Invalid record type: {0}".format(type(record)))

        if record.validate():
            self._records.append(record)
        else:
            raise InvalidDNSRecordException(u"Invalid record. Record: {0}".format(type(record)))

        return True

    def validate(self) -> bool:
        recs = self.get_records()

        if len(recs) == 0:
            return False

        has_soa = False
        nameserver_count = 0

        for rec in recs:
            if isinstance(rec, DNSSoaRecord):
                has_soa = True
            elif isinstance(rec, DNSNsRecord):
                nameserver_count += 1

        if has_soa and nameserver_count >= 1:
            return True

        return False

    def __str__(self) -> str:
        o = ""
        for i in self.get_records():
            o += u"{0}\n".format(i)
        return o
