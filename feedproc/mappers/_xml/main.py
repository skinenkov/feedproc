# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re

from ..base import MapperBase
from ..exceptions import FeedProcMapperRulesError
from feedproc.settings import LOGGER


class MapperXml(MapperBase):
    def __init__(self):
        super().__init__()

    def map_entities(self, data, entities):
        '''Method for processing xml-document into user-defined entities
        Args:
            data (str): xml-string
            entities (set of feedproc.entity.Entity): set of objects for mapping
        Returns:
            None
            Method modifies entities with mapped data
        '''
        data = self.clear_namespaces(data)
        for entity in entities:
            xml = ET.fromstring(data)
            for item in xml.findall(entity.wrapper):
                d = dict()
                for field, rule in entity.fields.items():
                    use_attr = False
                    attr = None
                    field_name = field
                    if '__' in field:
                        use_attr = True
                        arr = field.split('__')
                        attr = arr[1]
                        field_name = arr[0]
                    elem = item.findall(rule)
                    if elem is None or len(elem) == 0:
                        continue
                    if len(elem) == 1:
                        elem = elem[0]
                        val = elem.text if not use_attr else elem.attrib[attr]
                    else:
                        val = [el.text if not use_attr else el.attrib[attr] for el in elem]
                    d[field_name] = val
                entity.append_data(d)

    def to_json(self, xmldata):
        '''Method for converting xml-document into dict
        Args:
            xmldata (str): xml-string for processing
        Returns:
            (dict): dictionary (json)
        '''

        data = self.clear_namespaces(xmldata)
        xml = ET.fromstring(data)

        def parse_tree(el):
            response = {}
            for item in list(el):
                if list(item):
                    value = parse_tree(item)
                else:
                    value = item.text
                if item.tag in response:
                    if not isinstance(response[item.tag], list):
                        response[item.tag] = [response[item.tag]]
                    response[item.tag].append(value)
                else:
                    response[item.tag] = value
            return response
        processed = parse_tree(xml)
        return processed

    @staticmethod
    def assert_rules(rules):
        if not 'content' in rules:
            raise FeedProcMapperRulesError('"content" key required in rules')
        if not 'wrapper_entity' in rules['content']:
            raise FeedProcMapperRulesError('"wrapper_entity" key required in rules["content"]')
        if not 'fields' in rules['content']:
            raise FeedProcMapperRulesError('"fields" key required in rules["content"]')
        if not rules['content']['fields']:
            raise FeedProcMapperRulesError('"fields" must not be empty')
        if not isinstance(rules['content']['fields'], dict):
            raise FeedProcMapperRulesError('"fields" must be a dictionary')

    @staticmethod
    def clear_namespaces(xml):
        return re.sub(' xmlns="[^"]+"', '', xml, count=1)

    @property
    def type(self):
        return 'xml'
