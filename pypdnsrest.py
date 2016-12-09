# -*- coding: utf8 -*-
import logging

log = logging.getLogger(__name__)

if __name__ == "__main__":
    # Example:
    import sys

    logging.basicConfig(
        stream=sys.stdout,
        # level=logging.DEBUG
    )

    from pypdnsrest.client import PowerDnsRestApiClient

    zone = u"example.org."

    api = PowerDnsRestApiClient(u"pdnsapi")

    try:
        api.del_zone(zone)
    except:
        pass

    api.add_zone(zone, [
        "ns1.{0}".format(zone),
        "ns2.{0}".format(zone),
    ])

    # Add SOA record
    from pypdnsrest.dnsrecords import DNSSoaRecord
    from pypdnsrest.dnsrecords import DNSSoaRecordData

    serial = -1
    for i in api.get_zone(zone).get_records():
        if isinstance(i, DNSSoaRecord):
            recdata = i.get_data()
            if isinstance(recdata, DNSSoaRecordData):
                serial = recdata.get_data()['serial']

    soadata = DNSSoaRecordData("ns1.{0}".format(zone), "admin.{0}".format(zone), serial + 1)
    rec = DNSSoaRecord(zone)
    rec.set_data(soadata)
    api.add_record(zone, rec)

    # Add NS records
    from pypdnsrest.dnsrecords import DNSNsRecord

    rec = DNSNsRecord(zone)
    rec.set_data("ns1.{0}".format(zone))
    api.add_record(zone, rec)

    rec = DNSNsRecord(zone)
    rec.set_data("ns2.{0}".format(zone))
    api.add_record(zone, rec)

    # Add A records
    from ipaddress import IPv4Address
    from pypdnsrest.dnsrecords import DNSARecord

    rec = DNSARecord(zone)
    rec.set_data(IPv4Address("192.168.0.1"))
    api.add_record(zone, rec)

    rec = DNSARecord("ns1.{0}".format(zone))
    rec.set_data(IPv4Address("192.168.0.1"))
    api.add_record(zone, rec)

    rec = DNSARecord("ns2.{0}".format(zone))
    rec.set_data(IPv4Address("192.168.0.1"))
    api.add_record(zone, rec)

    # Add PTR record
    from pypdnsrest.dnsrecords import DNSPtrRecord

    rec = DNSPtrRecord(zone)
    rec.set_data(IPv4Address("192.168.101.1"))
    api.add_record(zone, rec)

    zonedata = api.get_zone(zone)
    recs = zonedata.get_records()
    for i in recs:
        print(i)

    api.del_zone(zone)
