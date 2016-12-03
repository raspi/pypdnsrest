# -*- coding: utf8 -*-


class RecordParser():
    """
    Base parser class
    """

    def parse(self, data):
        raise NotImplementedError("Parser not implemented.")


class SoaRecordParser(RecordParser):
    def parse(self, data):
        from datetime import timedelta
        from pypdnsrest.dnsrecords import DNSSoaRecord
        from pypdnsrest.dnsrecords import DNSSoaRecordData

        tmp = data['records'][0]['content'].split(" ")
        d = DNSSoaRecordData(nameserver=tmp[0], email=tmp[1], serial=int(tmp[2]),
                             ttl=timedelta(seconds=data['ttl']))
        rec = DNSSoaRecord(data['name'])
        rec.set_data(d)
        return rec


class MxRecordParser(RecordParser):
    def parse(self, data):
        from pypdnsrest.dnsrecords import DNSMxRecord
        from pypdnsrest.dnsrecords import DNSMxRecordData

        tmp = data['records'][0]['content'].split(" ")
        d = DNSMxRecordData(priority=tmp[0], server=tmp[1])
        rec = DNSMxRecord(data['name'])
        rec.set_data(d)
        return rec


class ARecordParser(RecordParser):
    def parse(self, data):
        from ipaddress import IPv4Address
        from pypdnsrest.dnsrecords import DNSARecord
        rec = DNSARecord(data['name'])
        rec.set_data(IPv4Address(data['records'][0]['content']))
        return rec


class AaaaRecordParser(RecordParser):
    def parse(self, data):
        from ipaddress import IPv6Address
        from pypdnsrest.dnsrecords import DNSAaaaRecord
        rec = DNSAaaaRecord(data['name'])
        rec.set_data(IPv6Address(data['records'][0]['content']))
        return rec


class CnameRecordParser(RecordParser):
    def parse(self, data):
        from pypdnsrest.dnsrecords import DNSCNameRecord
        rec = DNSCNameRecord(data['name'])
        rec.set_data(data['records'][0]['content'])
        return rec


class NsRecordParser(RecordParser):
    def parse(self, data):
        from pypdnsrest.dnsrecords import DNSNsRecord
        rec = DNSNsRecord(data['name'])
        rec.set_data(data['records'][0]['content'])
        return rec
