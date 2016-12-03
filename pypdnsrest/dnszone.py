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


class DNSZoneBase:
    pass


class DNSZone(DNSZoneBase):
    _records = []

    def add_record(self, record: DNSRecordMainBase):

        if not isinstance(record, DNSRecordMainBase):
            raise InvalidDNSRecordException("Invalid record type")

        if record.validate():
            self._records.append(record)
            log.debug("Added: {0}".format(record))
        else:
            raise InvalidDNSRecordException("Invalid record")

    def get_records(self):
        return self._records

    def validate(self):
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

    def __str__(self):
        o = ""
        for i in self.get_records():
            o += u"{0}\n".format(i)
        return o
