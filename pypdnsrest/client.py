# -*- coding: utf8 -*-
import logging

log = logging.getLogger(__name__)

from pprint import pprint
import json

from requests import Session
from requests.models import Response
from requests.models import PreparedRequest

from pypdnsrest.dnsrecords import DNSRecordMainBase
from pypdnsrest.dnsrecords import InvalidDNSRecordException

from pypdnsrest.dnszone import DNSZone

from pypdnsrest.parsers import RecordParser


class PowerDnsRestApiException(Exception):
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

    def __init__(self, apikey: str, protocol: str = u"http", host: str = u"127.0.0.1", port: int = 8081,
                 path: str = u"/api/v1/servers/localhost/"):
        self._rec_parsers = []
        self._host = host
        self._port = port
        self._protocol = protocol
        self._path = path
        self._apikey = apikey
        self.c = Session()

        self.c.hooks = {
            'response': self._hook_response,
        }

    def _request_to_str(self, req: PreparedRequest) -> str:
        o = u"-- REQUEST {0} @ {1}\n".format(req.method, req.url)
        o += u"{0}\n".format(pprint(req.headers))

        body = req.body

        try:
            body = json.dumps(json.loads(body), indent=4)
        except Exception:
            pass

        o += u"{0}\n".format(body)
        return o

    def _response_to_str(self, res: Response) -> str:
        o = u"-- RESPONSE ({0}):\n".format(res.status_code)
        o += u"{0}\n".format(pprint(res.headers))

        jsondata = None

        try:
            jsondata = res.json()
        except:
            pass

        if jsondata is not None:
            o += u"{0}\n".format(json.dumps(jsondata, indent=4))
        else:
            o += u"{0}\n".format(res.content)

        return o

    def _hook_response(self, response: Response, *args, **kw):
        o = "\n{0}".format(self._request_to_str(response.request))
        o += "\n{0}".format(self._response_to_str(response))

        o += "\n"

        log.debug(o)

        if response.status_code >= 400:
            try:
                err = json.dumps(response.json(), indent=4)
            except:
                err = getattr(response, "content", None)

            if err is None:  # pragma: no cover
                err = response.raw

            raise PowerDnsRestApiException(err)

    def _get_ses(self, url, data=None) -> dict:
        headers = {
            'X-API-Key': self._apikey,
        }

        url = u"{0}://{1}:{2}{3}{4}".format(self._protocol, self._host, self._port, self._path, url)

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

    def get_zones(self) -> list:
        return self._req_get("zones").json()

    def add_zone(self, name: str, nameservers: list) -> bool:

        if not isinstance(nameservers, list):
            raise TypeError(u"Wrong type. List was excepted.")

        if len(nameservers) == 0:
            raise ValueError(u"No name server(s) listed.")

        for i in nameservers:
            if i is None:
                raise TypeError(u"Wrong type. str was excepted. None given.")

            if not isinstance(i, str):
                raise TypeError(u"Wrong type. str was excepted.")

            if i == "":
                raise ValueError(u"Empty name server given")

        zone = {
            "name": name,
            "kind": u"Native",
            "masters": [],
            "nameservers": nameservers,
        }

        self._req_post(u"zones", data=json.dumps(zone))

        return True

    def add_parser(self, parser: RecordParser) -> bool:
        parsername = type(parser).__name__

        if not isinstance(parser, RecordParser):
            raise TypeError(u"Wrong parser type. RecordParser was expected. '{0}' was given.".format(parsername))

        parsers = self.get_parsers()
        parsernames = []

        for i in parsers:
            parsernames.append(parsername)

        if parsername not in parsernames:
            self._rec_parsers.append(parser)

        return len(self.get_parsers()) > 0

    def get_parsers(self) -> list:
        return self._rec_parsers

    def _load_default_parsers(self) -> bool:
        import inspect
        import pypdnsrest.parsers

        for name, obj in inspect.getmembers(pypdnsrest.parsers):
            if name.lower().find(u"RecordParser".lower()) == -1:
                continue
            if inspect.isclass(obj) and not inspect.isbuiltin(obj) and object not in obj.__bases__:
                inst = obj()
                if isinstance(inst, RecordParser):  # pragma: no cover
                    self.add_parser(inst)

        if len(self.get_parsers()) == 0:  # pragma: no cover
            raise ImportError(u"Couldn't load default parsers")

        return True

    def _get_zone_json(self, name: str) -> str:
        return self._req_get(u"zones/{0}".format(name)).json()

    def get_zone(self, name: str) -> DNSZone:

        zonedata = self._get_zone_json(name)

        o = DNSZone()

        if len(self.get_parsers()) == 0:
            self._load_default_parsers()

        for i in zonedata['rrsets']:

            parsername = u"{0}RecordParser".format(i['type'].title())

            for recs in i['records']:
                for parser in self.get_parsers():
                    if type(parser).__name__.lower() == parsername.lower():
                        try:
                            o.add_record(parser.parse(i['name'], recs['content'], int(i['ttl'])))
                        except Exception as exc:
                            log.warning(u"Parser error: {0}. Parser: {1}.".format(exc, type(parser).__name__))
                            raise

        return o

    def del_zone(self, zone: str) -> bool:
        self._req_delete(u"zones/{0}".format(zone))
        return True

    def _generate_record(self, record: dict, changetype: str = u"REPLACE") -> dict:
        if changetype.lower() not in [u'replace', u'delete']:  # pragma: no cover
            raise ValueError(u"Invalid value for changetype: '{0}'.".format(changetype))  # pragma: no cover

        rec = {"rrsets": [{
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

        if changetype.lower() is not u'delete':  # pragma: no cover
            rec['rrsets'][0]["ttl"] = record['ttl']  # pragma: no cover

        return rec

    def del_record(self, zone: str, record: DNSRecordMainBase) -> bool:
        if not isinstance(record, DNSRecordMainBase):
            raise TypeError("Invalid type for record: '{0}'.".format(type(record)))

        if not record.validate():
            raise InvalidDNSRecordException(u"Invalid record.")

        rec = self._generate_record(record.get_record(), u'delete')
        self._req_patch(u"zones/{0}".format(zone), data=json.dumps(rec))
        return True

    def _merge_record(self, zone: str, rec: dict) -> dict:
        if rec['rrsets'][0]['type'].lower() == u"SOA".lower():
            return rec

        for rrset in self._get_zone_json(zone)['rrsets']:
            same_type = rrset['type'].lower() == rec['rrsets'][0]['type'].lower()
            same_name = rrset['name'] == rec['rrsets'][0]['name'].lower()

            if same_type and same_name:
                for i in rrset['records']:
                    if i not in rec['rrsets'][0]['records']:
                        rec['rrsets'][0]['records'].append(i)

        return rec

    def add_record(self, zone: str, record: DNSRecordMainBase) -> bool:
        if not isinstance(record, DNSRecordMainBase):
            raise TypeError("Invalid type for record: '{0}'.".format(type(record)))

        if not record.validate():
            raise InvalidDNSRecordException(u"Invalid record. Type: {0} Data: {1}".format(type(record), record))

        rrdata = record.get_record()
        rec = self._generate_record(rrdata, u'replace')
        rec = self._merge_record(zone, rec)
        data = json.dumps(rec)
        self._req_patch(u"zones/{0}".format(zone), data=data)
        return True
