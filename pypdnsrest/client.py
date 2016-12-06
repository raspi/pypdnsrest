# -*- coding: utf8 -*-
import logging

log = logging.getLogger(__name__)

from pprint import pprint
import json

from requests import Session
from requests.models import Response

from pypdnsrest.dnsrecords import DNSRecordMainBase
from pypdnsrest.dnsrecords import InvalidDNSRecordException

from pypdnsrest.dnszone import DNSZoneInvalidException
from pypdnsrest.dnszone import DNSZone

from pypdnsrest.parsers import RecordParser


class PowerDnsRestApiException(Exception):
    pass


class PowerDnsRestApiCall():
    pass


class PowerDnsRestApiClient:
    """
    https://doc.powerdns.com/md/httpapi/api_spec/
    """

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
        req = response.request
        str = "\n-- REQUEST:\n"
        str += "{0} {1}\n".format(req.method, req.url)
        str += "{0}\n".format(pprint(req.headers))

        body = req.body

        try:
            body = json.dumps(json.loads(body), indent=4)
        except:
            pass

        str += "{0}\n".format(body)

        str += "\n-- RESPONSE ({0}):\n".format(response.status_code)
        str += "{0}\n".format(pprint(response.headers))

        jsondata = None

        try:
            jsondata = response.json()
        except:
            pass

        if jsondata is not None:
            str += "{0}\n".format(json.dumps(jsondata, indent=4))
        else:
            str += "{0}\n".format(response.content)

        str += "\n"

        log.debug(str)

        if response.status_code >= 400:
            try:
                err = json.dumps(response.json(), indent=4)
            except:
                err = getattr(response, "content", None)

            if err is None:
                err = response.raw

            raise PowerDnsRestApiException(err)


    def _get_ses(self, url, data=None) -> dict:
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


    def _req_get(self, url) -> Response:
        """
        GET
        :param url:
        :return:
        """

        s = self._get_ses(url)

        r = self.c.get(s['url'], headers=s['headers'])

        return r

    def _req_post(self, url, data=None) -> Response:
        """
        POST
        :param url:
        :param data:
        :return:Response
        """

        s = self._get_ses(url, data)
        r = self.c.post(s['url'], headers=s['headers'], data=s['data'])
        return r

    def _req_patch(self, url, data=None) -> Response:
        """
        PATCH
        :param url:
        :param data:
        :return:Response
        """

        s = self._get_ses(url, data)
        r = self.c.patch(s['url'], headers=s['headers'], data=s['data'])
        return r

    def _req_delete(self, url) -> Response:
        """
        DELETE
        :param url:
        :return:
        """

        s = self._get_ses(url)
        r = self.c.delete(s['url'], headers=s['headers'])
        return r


    def get_zones(self) -> str:
        return self._req_get("zones").json()

    def add_zone(self, name: str, nameservers: list):

        if not isinstance(nameservers, list):
            raise ValueError("Wrong type. List was excepted.")

        if len(nameservers) == 0:
            raise ValueError("No name server(s) listed.")

        for i in nameservers:
            if i is None or i is "":
                raise ValueError("Empty name server given")

        zone = {
            "name": name,
            "kind": "Native",
            "masters": [],
            "nameservers": nameservers,
        }

        req = self._req_post("zones", data=json.dumps(zone))

        return True

    def add_parser(self, parser: RecordParser):
        if not isinstance(parser, RecordParser):
            raise TypeError("Wrong parser type. RecordParser was expected.")

        if parser not in self.get_parsers():
            self._rec_parsers.append(parser)
        return True

    def get_parsers(self) -> list:
        return self._rec_parsers

    def _load_default_parsers(self):
        import inspect
        import pypdnsrest.parsers

        for name, obj in inspect.getmembers(pypdnsrest.parsers):
            if name.lower().find("RecordParser".lower()) == -1:
                continue
            if inspect.isclass(obj) and not inspect.isbuiltin(obj) and object not in obj.__bases__:
                inst = obj()
                if isinstance(inst, RecordParser):
                    self.add_parser(inst)

        if len(self.get_parsers()) == 0:
            raise ImportError("Couldn't load default parsers")

        return True

    def _get_zone_json(self, name: str) -> str:
        return self._req_get("zones/{0}".format(name)).json()


    def get_zone(self, name: str) -> DNSZone:

        zonedata = self._get_zone_json(name)

        o = DNSZone()

        if len(self.get_parsers()) == 0:
            self._load_default_parsers()

        for i in zonedata['rrsets']:

            parsername = "{0}RecordParser".format(i['type'].title())

            for recs in i['records']:
                try:
                    for parser in self.get_parsers():
                        if type(parser).__name__.lower() == parsername.lower():
                            o.add_record(parser.parse(i['name'], recs, i['ttl']))
                except Exception as exc:
                    log.warning("Parser error: %s", exc)

        if o.validate():
            return o

        raise DNSZoneInvalidException("Invalid zone.")

    def del_zone(self, zone:str):
        r = self._req_delete("zones/{0}".format(zone))
        return True


    def _generate_record(self, record:dict, changetype:str="REPLACE") -> dict:
        if changetype.lower() not in ['replace', 'delete']:
            raise ValueError("Invalid value for changetype: '{0}'.".format(changetype))

        rec =  {"rrsets": [{
            "name": record['name'],
            "type": record['type'],
            "changetype": changetype.upper(),
            "records": [
                {
                    "content": record['data'],
                    "disabled": False,
                },
            ],
        }, ], }

        if changetype.lower() is not 'delete':
            rec['rrsets'][0]["ttl"] = record['ttl']

        return rec


    def del_record(self, zone:str, record:DNSRecordMainBase):
        if not isinstance(record, DNSRecordMainBase):
            raise InvalidDNSRecordException()

        if not record.validate():
            raise InvalidDNSRecordException("Invalid record.")

        rec = self._generate_record(record.get_record(), 'delete')

        req = self._req_patch("zones/{0}".format(zone), data=json.dumps(rec))

        return req

    def add_record(self, zone: str, record: DNSRecordMainBase):
        if not isinstance(record, DNSRecordMainBase):
            raise InvalidDNSRecordException()

        if not record.validate():
            raise InvalidDNSRecordException("Invalid record.")

        rrdata = record.get_record()
        rec = self._generate_record(rrdata, 'replace')

        zonerrsets = self._get_zone_json(zone)['rrsets']

        for rrset in zonerrsets:
            if rrset['type'].lower() == rec['rrsets'][0]['type'].lower() and rrset['name'] == rec['rrsets'][0]['name'].lower():
                for i in rrset['records']:
                    if i not in rec['rrsets'][0]['records']:
                        rec['rrsets'][0]['records'].append(i)

        data = json.dumps(rec)

        #print(json.dumps(json.loads(data), indent=4))

        req = self._req_patch("zones/{0}".format(zone), data=data)

        return True
