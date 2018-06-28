# -*- coding: utf-8 -*-

from .settings import LOGGER
from .source import Source


class Parser(object):
    def __init__(self):
        self.sources = set()

    def add_source(self, source):
        self.sources.add(source)

    def run(self):
        for s in self.sources:
            s.clear_previous()
            data = s.process_data()
            #LOGGER.info('processed %s', s.parsed_entities)


