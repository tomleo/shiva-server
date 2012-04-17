# -*- coding: utf-8 -*-
from . import persistence


class PersistentObject(object):

    def __init__(self, **kwargs):
        self.db = kwargs['session']
        del(kwargs['session'])
        if 'instance' in kwargs:
            self.instance = kwargs.get('instance')
        else:
            self.instance = self.PersistentClass(**kwargs)

    def __getattribute__(self, name):
        try:
            return super(PersistentObject, self).__getattribute__(name)
        except AttributeError:
            return self.instance.__getattribute__(name)

    def save(self):
        self.db.add(self.instance)
        self.db.commit()

    def delete(self):
        self.db.delete(self.instance)
        self.db.commit()

    @staticmethod
    def get_persistence():
        raise NotImplementedError


class User(PersistentObject):

    PersistentClass = persistence.User

    @staticmethod
    def get_persistence():
        return persistence.User
