#! /usr/bin/env python3
import logging

import vigilante

logger = logging.getLogger('vigilante')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/vigilante.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
# logging.disable(logging.DEBUG)


vigilante.main()
