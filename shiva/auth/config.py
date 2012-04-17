# -*- coding: utf-8 -*-
import os

import shiva
from shiva import config as _config, settings


config = _config.Config(os.path.dirname(shiva.__file__))
config.from_object(settings)
