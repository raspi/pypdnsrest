# -*- coding: utf8 -*-

from datetime import timedelta
from ipaddress import IPv4Address
from ipaddress import IPv6Address


class InvalidDNSRecordException(ValueError):
    pass


class DNSRecordMainBase:
    record_ttl = timedelta(hours=1)

    def set_data(self, data, *args, **kwargs):
        raise NotImplementedError("Not implemented")

    def validate(self):
        raise NotImplementedError("Not implemented")


class DNSRecordBase(DNSRecordMainBase):
    record_type = None
    record_data = None
    record_name = None

    def __init__(self, name: str, ttl: timedelta = timedelta(seconds=0)):
        self.record_name = name

        if ttl.total_seconds() > 0:
            self.ttl = ttl

    def __str__(self):
        return u"{0} {1} {2} {3}".format(self.record_name, int(self.record_ttl.total_seconds()), self.record_type,
                                         self.record_data)

    def get_record(self):
        return {'ttl': self.record_ttl, 'type': self.record_type, 'data': self.record_data, 'name': self.record_name}

    def set_data(self, *args, **kwargs):
        raise NotImplementedError("Not implemented")

    def validate(self):
        raise NotImplementedError("Not implemented")


class DNSSoaRecordData(DNSRecordMainBase):
    nameserver = None
    email = None
    record_ttl = timedelta(hours=24)
    serial = -1

    def __init__(self, nameserver: str, email: str, serial: int = -1, ttl: timedelta = timedelta(seconds=0)):
        if not isinstance(ttl, timedelta):
            raise ValueError("Excepted 'ttl' to be datetime.timedelta object")

        if not isinstance(serial, int):
            raise ValueError("Excepted 'serial' to be int")

        self.nameserver = nameserver
        self.email = email
        self.serial = serial

        if ttl.total_seconds() > 0:
            self.record_ttl = ttl

        if not self.validate():
            raise InvalidDNSRecordException("Invalid SOA.")

    def __str__(self):
        return u"{0} {1} {2} {3} {3} {3} {3}".format(self.nameserver, self.email, self.serial,
                                                     int(self.record_ttl.total_seconds()))

    def validate(self):
        if self.email.count('.') <= 2:
            return False

        if int(self.record_ttl.total_seconds()) <= 1:
            return False

        if self.serial <= 0:
            return False

        if self.nameserver is None or self.nameserver is "":
            return False

        return True


class DNSARecord(DNSRecordBase):
    record_type = u'A'

    def set_data(self, data: IPv4Address):
        self.record_data = data

        if not self.validate():
            raise InvalidDNSRecordException("Invalid type. IPv4Address excepted.")

    def validate(self):
        if isinstance(self.record_data, IPv4Address):
            return True
        return False


class DNSAaaaRecord(DNSRecordBase):
    record_type = u'AAAA'

    def set_data(self, data: IPv6Address):
        self.record_data = data

        if not self.validate():
            raise InvalidDNSRecordException("Invalid type. IPv6Address excepted.")


class DNSNsRecord(DNSRecordBase):
    record_type = u'NS'

    def set_data(self, data: str):
        self.record_data = data

        if not self.validate():
            raise InvalidDNSRecordException("Invalid type. str excepted.")

    def validate(self):
        if isinstance(self.record_data, str):
            return True
        return False


class DNSCNameRecord(DNSRecordBase):
    record_type = u'CNAME'

    def set_data(self, data: str):
        self.record_data = data

        if not self.validate():
            raise InvalidDNSRecordException("Invalid type. str excepted.")

    def validate(self):
        if isinstance(self.record_data, str):
            return True
        return False


class DNSSoaRecord(DNSRecordBase):
    record_type = u'SOA'

    def set_data(self, data: DNSSoaRecordData):
        self.record_data = data

        if not self.validate():
            raise InvalidDNSRecordException("Invalid type. DNSSoaRecordData excepted.")

    def validate(self):
        if not isinstance(self.record_data, DNSSoaRecordData):
            return False
        return True


class DNSMxRecordData(DNSRecordMainBase):
    server = None
    priority = -1

    def __init__(self, server: str, priority: int, ttl: timedelta = timedelta(seconds=0)):
        if not isinstance(ttl, timedelta):
            raise ValueError("Excepted 'ttl' to be datetime.timedelta object")

        self.server = server
        self.priority = priority

        if not self.validate():
            raise InvalidDNSRecordException("Invalid data.")

    def validate(self):
        if not isinstance(self.record_data, DNSSoaRecordData):
            return False

        if self.priority <= 0:
            return False

        if self.server.count('.') < 1:
            return False

        return True


class DNSMxRecord(DNSRecordBase):
    record_type = u'MX'

    def set_data(self, data: DNSMxRecordData):
        if not isinstance(data, DNSMxRecordData):
            raise InvalidDNSRecordException("Invalid type. DNSMxRecordData excepted.")

        self.record_data = data

        if not self.validate():
            raise InvalidDNSRecordException("Invalid record.")

    def validate(self):
        if not isinstance(self.record_data, DNSMxRecordData):
            return False

        return True
