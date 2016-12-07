# -*- coding: utf8 -*-
"""
Convert REST JSON dict to DNSRecordBase classes
"""

import logging

log = logging.getLogger(__name__)

from pypdnsrest.dnsrecords import DNSRecordBase


class RecordParser():
    """
    Base parser class
    """

    def __init__(self, *args, **kwargs):
        pass

    def parse(self, name: str = "", data: list = [], ttl: int = 0) -> DNSRecordBase:
        raise NotImplementedError("Parser not implemented.")


class SoaRecordParser(RecordParser):
    def parse(self, name: str, data: list, ttl: int) -> DNSRecordBase:
        from datetime import timedelta
        from pypdnsrest.dnsrecords import DNSSoaRecord
        from pypdnsrest.dnsrecords import DNSSoaRecordData

        tmp = data['content'].split(" ")
        d = DNSSoaRecordData(nameserver=tmp[0], email=tmp[1], serial=int(tmp[2]), refresh=timedelta(seconds=tmp[3]),
                             retry=timedelta(seconds=tmp[4]), expire=timedelta(seconds=tmp[4]),
                             ttl=timedelta(seconds=tmp[5]))
        rec = DNSSoaRecord(name)
        rec.set_data(d)
        return rec


class MxRecordParser(RecordParser):
    def parse(self, name: str, data: list, ttl: int) -> DNSRecordBase:
        from pypdnsrest.dnsrecords import DNSMxRecord
        from pypdnsrest.dnsrecords import DNSMxRecordData

        tmp = data['content'].split(" ")
        d = DNSMxRecordData(priority=tmp[0], server=tmp[1])
        rec = DNSMxRecord(name)
        rec.set_data(d)
        return rec


class ARecordParser(RecordParser):
    def parse(self, name: str, data: list, ttl: int) -> DNSRecordBase:
        from ipaddress import IPv4Address
        from pypdnsrest.dnsrecords import DNSARecord
        rec = DNSARecord(name)
        rec.set_data(IPv4Address(data['content']))
        return rec


class AaaaRecordParser(RecordParser):
    def parse(self, name: str, data: list, ttl: int) -> DNSRecordBase:
        from ipaddress import IPv6Address
        from pypdnsrest.dnsrecords import DNSAaaaRecord
        rec = DNSAaaaRecord(name)
        rec.set_data(IPv6Address(data['content']))
        return rec


class CnameRecordParser(RecordParser):
    def parse(self, name: str, data: list, ttl: int) -> DNSRecordBase:
        from pypdnsrest.dnsrecords import DNSCNameRecord
        rec = DNSCNameRecord(name)
        rec.set_data(data['content'])
        return rec


class NsRecordParser(RecordParser):
    def parse(self, name: str, data: list, ttl: int) -> DNSRecordBase:
        from pypdnsrest.dnsrecords import DNSNsRecord
        rec = DNSNsRecord(name)
        rec.set_data(data['content'])
        return rec


class PtrRecordParser(RecordParser):
    def parse(self, name: str, data: list, ttl: int) -> DNSRecordBase:
        from pypdnsrest.dnsrecords import DNSPtrRecord
        cont = ".".join(data['content'].lower().replace("in-addr.arpa", '').strip(".").split('.')[::-1])

        if cont.count(".") == 3:
            from ipaddress import IPv4Address
            cont = IPv4Address(cont)
        else:
            from ipaddress import IPv6Address
            cont = IPv6Address(cont)

        rec = DNSPtrRecord(name)
        rec.set_data(cont)
        return rec
