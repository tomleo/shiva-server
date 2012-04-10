# -*- coding: utf-8 -*-
from os import path

DEBUG = True

PROJECT_ROOT = path.dirname(path.abspath(__file__))[:-len('/settings')]
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/stream.db' % PROJECT_ROOT
ACCEPTED_FORMATS = {
    'Audio': ('flac', 'm4a', 'mp3', 'ogg', 'wav', 'wma'),
    'Video': ('3gp', 'avi', 'divx', 'flv', 'm4p', 'mov', 'mp4', 'mpeg', 'mpg',
              'rmvb', 'webm', 'wmv'),
}
