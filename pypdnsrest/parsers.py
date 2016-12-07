# -*- coding: utf8 -*-
"""
Convert REST JSON dict to DNSRecordBase classes
"""

import logging

log = logging.getLogger(__name__)

from datetime import timedelta
from pypdnsrest.dnsrecords import DNSRecordBase


class RecordParser():
    """
    Base parser class
    """

    def __init__(self, *args, **kwargs):
        pass

    def parse(self, name: str, data: str, ttl: int) -> DNSRecordBase:
        raise NotImplementedError(u"Parser not implemented.")


class SoaRecordParser(RecordParser):
    def parse(self, name: str, data: str, ttl: int) -> DNSRecordBase:
        from pypdnsrest.dnsrecords import DNSSoaRecord
        from pypdnsrest.dnsrecords import DNSSoaRecordData

        if data.count(u" ") != 6:
            raise ValueError("Invalid value: '{0}'".format(data))

        tmp = data.split(" ")
        d = DNSSoaRecordData(nameserver=tmp[0], email=tmp[1], serial=int(tmp[2]),
                             refresh=timedelta(seconds=int(tmp[3])),
                             retry=timedelta(seconds=int(tmp[4])), expire=timedelta(seconds=int(tmp[4])),
                             ttl=timedelta(seconds=int(tmp[5])))
        rec = DNSSoaRecord(name, timedelta(seconds=ttl))
        rec.set_data(d)
        return rec


class MxRecordParser(RecordParser):
    def parse(self, name: str, data: str, ttl: int) -> DNSRecordBase:
        from pypdnsrest.dnsrecords import DNSMxRecord
        from pypdnsrest.dnsrecords import DNSMxRecordData

        tmp = data.split(" ")
        d = DNSMxRecordData(priority=tmp[0], server=tmp[1])
        rec = DNSMxRecord(name, timedelta(seconds=ttl))
        rec.set_data(d)
        return rec


class ARecordParser(RecordParser):
    def parse(self, name: str, data: str, ttl: int) -> DNSRecordBase:
        from ipaddress import IPv4Address
        from pypdnsrest.dnsrecords import DNSARecord
        rec = DNSARecord(name, timedelta(seconds=ttl))
        rec.set_data(IPv4Address(data))
        return rec


class AaaaRecordParser(RecordParser):
    def parse(self, name: str, data: str, ttl: int) -> DNSRecordBase:
        from ipaddress import IPv6Address
        from pypdnsrest.dnsrecords import DNSAaaaRecord
        rec = DNSAaaaRecord(name, timedelta(seconds=ttl))
        rec.set_data(IPv6Address(data))
        return rec


class CnameRecordParser(RecordParser):
    def parse(self, name: str, data: str, ttl: int) -> DNSRecordBase:
        from pypdnsrest.dnsrecords import DNSCNameRecord
        rec = DNSCNameRecord(name, timedelta(seconds=ttl))
        rec.set_data(data)
        return rec


class NsRecordParser(RecordParser):
    def parse(self, name: str, data: str, ttl: int) -> DNSRecordBase:
        from pypdnsrest.dnsrecords import DNSNsRecord
        rec = DNSNsRecord(name, timedelta(seconds=ttl))
        rec.set_data(data)
        return rec


class PtrRecordParser(RecordParser):
    def parse(self, name: str, data: str, ttl: int) -> DNSRecordBase:
        if data.lower().find("in-addr.arpa.") == -1:
            raise ValueError(u"Invalid PTR value: '{0}'".format(data))

        from pypdnsrest.dnsrecords import DNSPtrRecord
        cont = ".".join(data.lower().replace("in-addr.arpa", '').strip(".").split('.')[::-1])

        if cont.count(".") == 3:
            from ipaddress import IPv4Address
            cont = IPv4Address(cont)
        else:
            from ipaddress import IPv6Address
            cont = IPv6Address(cont)

        rec = DNSPtrRecord(name, timedelta(seconds=ttl))
        rec.set_data(cont)
        return rec
