# -*- coding: utf8 -*-
import logging

log = logging.getLogger(__name__)

import json

from requests import Session
from requests.models import Response

from pypdnsrest.dnsrecords import DNSRecordMainBase
from pypdnsrest.dnsrecords import InvalidDNSRecordException

from pypdnsrest.dnszone import DNSZoneInvalidException

from pypdnsrest.parsers import RecordParser


class PowerDnsRestApiException(Exception):
    pass


class PowerDnsRestApiCall():
    pass


class PowerDnsRestApiClient:
    _host = None
    _port = None
    _apikey = None
    _path = None
    _protocol = None

    c = Session()

    _rec_parsers = []

    def __init__(self, apikey: str, protocol: str = "http", host: str = "127.0.0.1", port: int = 8081,
                 path: str = "/api/v1/servers/localhost/"):
        self._host = host
        self._port = port
        self._protocol = protocol
        self._path = path
        self._apikey = apikey
        self.c = Session()
        self.c.hooks = {
            'response': self._hook_response,
        }

    def _hook_response(self, response: Response, *args, **kw):
        log.debug("RESPONSE: {0} {1} {3}\n\t\t{2}".format(response.request.method, response.status_code, response.url,
                                                          response.content))

    def _get_ses(self, url, data=None):
        headers = {
            'X-API-Key': self._apikey,
        }

        url = "{0}://{1}:{2}{3}{4}".format(self._protocol, self._host, self._port, self._path, url)

        o = {
            'headers': headers,
            'url': url,
            'data': data,
        }

        return o

    def _req_get(self, url):
        """
        GET
        :param url:
        :return:
        """

        s = self._get_ses(url)

        r = self.c.get(s['url'], headers=s['headers'])
        return r

    def _req_post(self, url, data=None):
        """
        POST
        :param url:
        :param data:
        :return:Response
        """

        s = self._get_ses(url, data)
        r = self.c.post(s['url'], headers=s['headers'], data=s['data'])
        return r

    def _req_patch(self, url, data=None):
        """
        PATCH
        :param url:
        :param data:
        :return:Response
        """

        s = self._get_ses(url, data)
        r = self.c.patch(s['url'], headers=s['headers'], data=s['data'])
        return r

    def get_zones(self):
        zones = self._req_get("zones")
        z = json.loads(zones.content.decode('utf8'))
        return z

    def add_zone(self, name: str, nameservers: list):

        if not isinstance(nameservers, list):
            raise Exception("Wrong type. List was excepted.")

        if len(nameservers) == 0:
            raise Exception("No name server(s) listed.")

        for i in nameservers:
            if i is None or i is "":
                raise Exception("Empty name server given")

        zone = {
            "name": name,
            "kind": "Native",
            "masters": [],
            "nameservers": nameservers,
        }

        req = self._req_post("zones", data=json.dumps(zone))

        if req.status_code >= 400:
            raise PowerDnsRestApiException(req.content)

        return req

    def add_parser(self, parser: RecordParser):
        if not isinstance(parser, RecordParser):
            raise TypeError("Wrong parser type. RecordParser was expected.")

        if parser not in self.get_parsers():
            self._rec_parsers.append(parser)
        return True

    def get_parsers(self):
        return self._rec_parsers

    def _load_default_parsers(self):
        import inspect
        import pypdnsrest.parsers

        for name, obj in inspect.getmembers(pypdnsrest.parsers):
            if inspect.isclass(obj) and not inspect.isbuiltin(obj) and object not in obj.__bases__:
                inst = obj()
                if isinstance(inst, RecordParser):
                    self.add_parser(inst)

        if len(self.get_parsers()) == 0:
            raise ImportError("Couldn't load default parsers")

        return True

    def get_zone(self, name: str):
        zonereq = self._req_get("zones/{0}".format(name))

        if zonereq.status_code >= 400:
            raise DNSZoneInvalidException(zonereq.content)

        zonedata = json.loads(zonereq.content.decode('utf8'))

        from pypdnsrest.dnszone import DNSZone

        o = DNSZone()

        if len(self.get_parsers()) == 0:
            self._load_default_parsers()

        for i in zonedata['rrsets']:

            parsername = "{0}RecordParser".format(i['type'].title())

            try:
                for parser in self.get_parsers():
                    if type(parser).__name__ == parsername:
                        o.add_record(parser.parse(i))
            except Exception as exc:
                log.warning("Parser error: %s", exc)

        if o.validate():
            return o

        raise DNSZoneInvalidException("Invalid zone.")

    def _generate_record(self, rectype: str, name: str, data: str, ttl: int):
        return {"rrsets": [{
            "name": name,
            "type": rectype,
            "ttl": ttl,
            "changetype": "REPLACE",
            "records": [
                {
                    "content": data,
                    "disabled": False,
                },
            ],
        }, ], }

    def add_record(self, zone: str, record: DNSRecordMainBase):
        if not isinstance(record, DNSRecordMainBase):
            raise InvalidDNSRecordException()

        if not record.validate():
            raise InvalidDNSRecordException("Invalid record.")

        rec = self._generate_record(record.record_type, record.record_name, str(record.record_data),
                                    int(record.record_ttl.total_seconds()))

        req = self._req_patch("zones/{0}".format(zone), data=json.dumps(rec))

        if req.status_code >= 400:
            raise PowerDnsRestApiException(req.content)

        return req
