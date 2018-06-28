# -*- coding: utf-8 -*-


class MapperBase(object):
    def __init__(self):
        self.entities = set()

    def is_valid(self):
        # TODO: make validation
        return True

    def map_fields(self, data):
        raise NotImplementedError()

    def add_entity(self, entity):
        self.entities.add(entity)

    def to_json(self, data):
        raise NotImplemented

    @property
    def type(self):
        raise NotImplemented
