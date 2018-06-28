# -*- coding: utf-8 -*-

import logging


LOGGER = logging.getLogger('main')
sh = logging.StreamHandler()
sh.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(sh)

