# -*- coding: utf8 -*-

import abc

from datetime import timedelta
from ipaddress import IPv4Address
from ipaddress import IPv6Address


class InvalidDNSRecordException(ValueError):
    pass


class DNSRecordMainBase:
    _errors = []
    _ttl = timedelta(hours=1)

    def _add_error(self, err) -> bool:
        self._errors.append(err)
        return True

    def _get_errors(self) -> list:
        return self._errors

    @abc.abstractmethod
    def set_data(self, *args, **kwargs) -> bool:
        raise NotImplementedError(u"Not implemented")

    def validate(self) -> bool:
        raise NotImplementedError(u"Not implemented")

    def get_record(self) -> dict:
        return {
            'ttl': int(self._ttl.total_seconds()),
            'type': self._type,
            'data': str(self._data),
            'name': str(self._name)
        }


class DNSRecordBase(DNSRecordMainBase):
    _type = None
    _data = None
    _name = None

    def __init__(self, name: str, ttl: timedelta = timedelta(seconds=0)):
        self._name = name

        if ttl.total_seconds() > 0:
            self._ttl = ttl

    def __str__(self) -> str:
        return u"{0} {1} {2} {3}".format(str(self._name), int(self._ttl.total_seconds()), self._type,
                                         str(self._data))

    def set_data(self, *args, **kwargs) -> bool:
        raise NotImplementedError(u"Not implemented")

    def validate(self) -> bool:
        raise NotImplementedError(u"Not implemented")

    def get_data(self):
        return self._data


class DNSARecord(DNSRecordBase):
    _type = u'A'

    def set_data(self, data: IPv4Address) -> bool:
        self._data = data

        if not self.validate():
            self._add_error(u"Invalid type.")
            raise InvalidDNSRecordException("\n".join(self._get_errors()))

        return True

    def validate(self) -> bool:
        if self._data is None:
            self._add_error(u"'None' given.")
            return False
        if not isinstance(self._data, IPv4Address):
            self._add_error(u"IPv4Address excepted.")
            return False
        return True


class DNSAaaaRecord(DNSRecordBase):
    _type = u'AAAA'

    def set_data(self, data: IPv6Address) -> bool:
        self._data = data

        if not self.validate():
            self._add_error(u"Invalid type.")
            raise InvalidDNSRecordException("\n".join(self._get_errors()))

        return True

    def validate(self) -> bool:
        if self._data is None:
            self._add_error(u"'None' given.")
            return False
        if not isinstance(self._data, IPv6Address):
            self._add_error(u"IPv6Address excepted.")
            return False
        return True


class DNSNsRecord(DNSRecordBase):
    _type = u'NS'

    def set_data(self, data: str) -> bool:
        self._data = data

        if not self.validate():
            self._add_error(u"Invalid type.")
            raise InvalidDNSRecordException("\n".join(self._get_errors()))

        return True

    def validate(self) -> bool:
        if self._data is None:
            self._add_error(u"'None' given.")
            return False

        if not isinstance(self._data, str):
            self._add_error(u"Data is not str.")
            return False

        if self._data == "":
            self._add_error(u"Empty string given.")
            return False

        if self._data.count(":") != 0:
            self._add_error(u"Record can't be IPv6 address.")
            return False

        if self._data.count(".") == 3:
            from ipaddress import AddressValueError

            try:
                IPv4Address(self._data)
                self._add_error(u"Record can't be IPv4 address.")
                return False
            except AddressValueError:
                pass

        return True


class DNSCNameRecord(DNSRecordBase):
    _type = u'CNAME'

    def set_data(self, data: str) -> bool:
        self._data = data

        if not self.validate():
            self._add_error("Invalid data.")
            raise InvalidDNSRecordException("\n".join(self._get_errors()))

        return True

    def validate(self) -> bool:
        if self._data is None:
            self._add_error(u"'None' given.")
            return False

        if not isinstance(self._data, str):
            self._add_error(u"Data is not str.")
            return False

        if self._data == "":
            self._add_error("Empty string given.")
            return False

        return True


class DNSSoaRecordData(DNSRecordMainBase):
    _nameserver = None
    _email = None
    _serial = -1
    _refresh = timedelta(hours=3)
    _retry = timedelta(hours=1)
    _expire = timedelta(days=7)
    _ttl = timedelta(hours=24)

    def __init__(self, nameserver: str, email: str, serial: int = -1, refresh: timedelta = timedelta(seconds=0),
                 retry: timedelta = timedelta(seconds=0), expire: timedelta = timedelta(seconds=0),
                 ttl: timedelta = timedelta(seconds=0)):
        self._nameserver = nameserver
        self._email = email
        self._serial = serial

        if refresh.total_seconds() > 0:
            self._refresh = refresh

        if retry.total_seconds() > 0:
            self._retry = retry

        if expire.total_seconds() > 0:
            self._expire = expire

        if ttl.total_seconds() > 0:
            self._ttl = ttl

    def __str__(self) -> str:
        return u"{0} {1} {2} {3} {4} {5} {6}".format(self._nameserver, self._email, self._serial,
                                                     int(self._refresh.total_seconds()),
                                                     int(self._retry.total_seconds()),
                                                     int(self._expire.total_seconds()), int(self._ttl.total_seconds()))

    def get_data(self) -> dict:
        return {
            'nameserver': self._nameserver,
            'email': self._email,
            'serial': self._serial,
            'refresh': self._refresh,
            'retry': self._retry,
            'expire': self._expire,
            'ttl': self._ttl,
        }

    def validate(self) -> bool:
        if not isinstance(self._nameserver, str):
            self._add_error(u"Excepted 'nameserver' to be str.")
            return False

        if not isinstance(self._serial, int):
            self._add_error(u"Excepted 'serial' to be int.")
            return False

        if not isinstance(self._email, str):
            self._add_error(u"Excepted 'email' to be str.")
            return False

        if self._email.count('.') <= 2:
            self._add_error(u"Email is missing dot(s) ('.').")
            return False

        if int(self._ttl.total_seconds()) <= 1:
            self._add_error(u"Invalid TTL.")
            return False

        if self._serial < 0:
            self._add_error(u"Invalid serial.")
            return False

        if self._nameserver == "":
            self._add_error(u"Empty nameserver.")
            return False

        return True


class DNSSoaRecord(DNSRecordBase):
    _type = u'SOA'

    def set_data(self, data: DNSSoaRecordData) -> bool:
        self._data = data

        if not self.validate():
            self._add_error("Invalid SOA record.")
            raise InvalidDNSRecordException("\n".join(self._get_errors()))

        return True

    def validate(self) -> bool:
        if self._data is None:
            self._add_error(u"'None' given.")
            return False

        if not isinstance(self._data, DNSSoaRecordData):
            self._add_error("Invalid instance.")
            return False

        if not self._data.validate():
            self._add_error("Invalid SOA data. Data: {0}.".format(self._data))
            return False

        return True

    def __str__(self) -> str:
        return "{0} {1}".format(self._name, self._data)


class DNSMxRecordData(DNSRecordMainBase):
    _server = None
    _priority = -1

    def __init__(self, server: str, priority: int, ttl: timedelta = timedelta(seconds=0)):
        self._server = server
        self._priority = priority

        if ttl.total_seconds() > 0:
            self.ttl = ttl

    def __str__(self) -> str:
        return u"{0} {1} {2}".format(self._priority, self._server, int(self._ttl.total_seconds()))

    def validate(self) -> bool:
        if not isinstance(self._server, str):
            self._add_error(u"Server is not str.")
            return False

        if not isinstance(self._priority, int):
            self._add_error(u"Priority is not int.")
            return False

        if self._priority <= 0:
            self._add_error(u"Priority is too low")
            return False

        if self._server.count('.') < 1:
            self._add_error(u"Dot(s) ('.') missing.")
            return False

        return True


class DNSMxRecord(DNSRecordBase):
    _type = u'MX'

    def set_data(self, data: DNSMxRecordData):
        self._data = data

        if not self.validate():
            self._add_error("Invalid record.")
            raise InvalidDNSRecordException("\n".join(self._get_errors()))

        return True

    def validate(self) -> bool:
        if self._data is None:
            self._add_error(u"'None' given.")
            return False

        if not isinstance(self._data, DNSMxRecordData):
            return False

        if not self._data.validate():
            self._add_error("Data is invalid. Data: {0}".format(self._data))
            return False

        return True


class DNSPtrRecord(DNSRecordBase):
    _type = u'PTR'

    def set_data(self, data) -> bool:
        self._data = data

        if not self.validate():
            self._add_error("Invalid record data.")
            raise InvalidDNSRecordException("\n".join(self._get_errors()))

        return True

    def validate(self) -> bool:
        if self._data is None:
            self._add_error(u"'None' given.")
            return False

        is_valid = False
        if isinstance(self._data, IPv4Address):
            is_valid = True
        elif isinstance(self._data, IPv6Address):
            is_valid = True
        else:
            self._add_error(u"IPv4Address or IPv6Address expected.")

        return is_valid

    def __str__(self) -> str:
        return u"{0} {1} {2} {3}".format(self._data.reverse_pointer, int(self._ttl.total_seconds()), self._type,
                                         self._name)

    def get_record(self) -> dict:
        return {'ttl': int(self._ttl.total_seconds()), 'type': self._type, 'name': self._name,
                'data': "{0}.".format(self._data.reverse_pointer)}


class DNSTxtRecord(DNSRecordBase):
    _type = u'TXT'

    def set_data(self, data: str) -> bool:
        self._data = data

        if not self.validate():
            self._add_error("Invalid record data.")
            raise InvalidDNSRecordException("\n".join(self._get_errors()))

        return True

    def validate(self) -> bool:
        if self._data is None:
            self._add_error(u"'None' given.")
            return False

        if not isinstance(self._data, str):
            self._add_error(u"str expected.")
            return False

        if self._data == "":
            self._add_error(u"empty string given.")
            return False

        return True
