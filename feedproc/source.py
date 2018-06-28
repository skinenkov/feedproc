# -*- coding: utf-8 -*-

from .mappers import MAPPERS
from .mappers.base import MapperBase
import requests
import os.path
from .settings import LOGGER
import random


class Source:
    __MAPPER_TYPES = ('xml',)

    def __init__(self, resource_type, src):
        self.resource_type = resource_type
        self.src = src
        self.mapper = None
        self.__validated = None
        self.__mapper_cls = None
        self.__initial_validation()
        self.__data = None
        self.__entities = set()

    @classmethod
    def fromHttp(cls, src):
        return cls('http', src)

    @classmethod
    def fromFile(cls, filepath):
        return cls('file', filepath)

    @classmethod
    def fromString(cls, sourcestring):
        return cls('string', sourcestring)

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @property
    def type(self):
        self.__assert(isinstance(self.mapper, MapperBase), 'Mapper not set yet')
        return self.mapper.type

    @type.setter
    def type(self, t):
        t = str(t).lower()
        self.__assert(t in self.__MAPPER_TYPES,
                      'Not valid type. Allowed: %s' % self.__MAPPER_TYPES)
        if t == 'xml':
            self.__mapper_cls = MAPPERS.XML
        self.__init_mapper()

    @property
    def __http_headers(self):
        return {'user-agent': 'testApp/%s' % random.randint(1, 100000)}

    @property
    def is_validated(self):
        return self.__validated and self.mapper is not None

    @property
    def parsed_entities(self):
        _d = {}
        for entity in self.__entities:
            _d[entity.wrapper] = entity.data
        return _d

    def to_json(self):
        self.__assert(self.is_validated, 'Source is not validated')
        self.extract_data()
        return self.mapper.to_json(self.data)

    def extract_data(self):
        self.__assert(self.is_validated, 'Source is not fully inited yet!')
        if self.data:
            return
        data = None
        if self.resource_type == 'http':
            req = requests.get(self.src, headers=self.__http_headers)
            if not req.status_code in (200, ):
                return None
            data = req.text
        elif self.resource_type == 'string':
            assert(self.data is not None)
            data = self.data
        elif self.resource_type == 'file':
            self.__assert(os.path.isfile(self.src), 'File %s not found' % self.src)
            data = open(self.src).read()
        self.data = data

    def process_data(self):
        self.extract_data()
        parsed_data = self.mapper.map_entities(self.data, self.__entities)
        if not parsed_data:
            return None
        return parsed_data

    def clear_previous(self):
        for entity in self.__entities:
            entity.clear()

    def __init_mapper(self):
        self.mapper = self.__mapper_cls()
        LOGGER.info('mapper %s inited' % self.mapper.type)

    def bind_entity(self, entity):
        if entity not in self.__entities:
            self.__entities.add(entity)

    def __initial_validation(self):
        self.__assert(self.resource_type in ('file', 'http', 'https', 'string'))
        if self.resource_type == 'file':
            self.__assert(os.path.isfile(self.src),
                          'file not recognized: %s' % str(self.src))
        elif self.resource_type in ('http', 'https'):
            response = requests.head(self.src, headers=self.__http_headers)
            self.__assert(300 > response.status_code >= 200,
                          'resource responses with status %s' % response.status_code)
        self.__validated = True

    def __assert(self, condition, msg=None):
        if msg:
            assert condition, msg
        else:
            assert condition


