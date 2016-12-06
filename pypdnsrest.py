# -*- coding: utf8 -*-
import logging

log = logging.getLogger(__name__)

if __name__ == "__main__":
    # Example:
    import sys

    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG
    )

    #from pypdnsrest.client import PowerDnsRestApiClient

    #api = PowerDnsRestApiClient("pdnsapi")
    #api.del_zone("home.lan.")

    # api.add_zone("home.lan.", ["ns1.home.lan.", ])

    # Add record
    #from ipaddress import IPv4Address
    #from pypdnsrest.dnsrecords import DNSARecord
    #rec = DNSARecord("gw.home.lan.")
    #rec.set_data(IPv4Address("192.168.101.1"))
    #api.add_record("home.lan.", rec)

    #from ipaddress import IPv4Address
    #from pypdnsrest.dnsrecords import DNSPtrRecord
    #rec = DNSPtrRecord("gw.home.lan.")
    #rec.set_data(IPv4Address("192.168.101.1"))
    #api.add_record("home.lan.", rec)

    #from pypdnsrest.dnsrecords import DNSNsRecord
    #rec = DNSNsRecord("home.lan.")
    #rec.set_data("ns1.home.lan.")
    #api.add_record("home.lan.", rec)

    #from pypdnsrest.dnsrecords import DNSNsRecord
    #rec = DNSNsRecord("home.lan.")
    #rec.set_data("ns2.home.lan.")
    #api.add_record("home.lan.", rec)


    #zone = api.get_zone("home.lan")
    #recs = zone.get_records()
    #for i in recs:
    #    print(i)

    # zone = api.get_zone("invalid.test")
    # recs = zone.get_records()
    # print(recs)
