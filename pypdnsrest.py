# -*- coding: utf8 -*-
import logging

log = logging.getLogger(__name__)


if __name__ == "__main__":
    # Example:
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    from pypdnsrest.client import PowerDnsRestApiClient
    api = PowerDnsRestApiClient("pdnsapi")
    # api.add_zone("home.lan.", ["ns1.home.lan."])

    # Add record
    from ipaddress import IPv4Address
    from pypdnsrest.dnsrecords import DNSARecord
    rec = DNSARecord("home.lan.")
    rec.set_data(IPv4Address("127.0.0.1"))
    api.add_record("home.lan.", rec)

    zone = api.get_zone("home.lan")
    recs = zone.get_records()

