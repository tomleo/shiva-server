# -*- coding: utf-8 -*-
from os import path

from sqlalchemy import create_engine, orm

from .auth import User
from .auth.persistence import Base
from .config import Config


class Shiva(object):

    def __init__(self, config_obj=None):
        self.root_path = path.dirname(__file__)
        self.config = Config(self.root_path)

        if config_obj:
            self.configure(config_obj)

    def _mkuser(self, **kwargs):
        return User(session=self.db['session'], **kwargs)

    def configure(self, config_obj):
        self.config.from_object(config_obj)
        self.config_db()

    def config_db(self):
        db_engine = create_engine(self.config['SQLALCHEMY_DATABASE_URI'],
                                  echo=False)
        Session = orm.sessionmaker(bind=db_engine)
        self.db = {'engine': db_engine, 'session': Session()}

    def new_user(self, **kwargs):
        return self._mkuser(**kwargs)

    def init_db(self):
        Base.metadata.create_all(self.db['engine'])

    def query(self, cls):
        return self.db['session'].query(cls.PersistentClass)

    def authenticate(self, email, password):
        # import ipdb; ipdb.set_trace()
        U = User.get_persistence()
        q = self.db['session'].query(U)
        q.filter_by(email=email, password=U.hash_password(password))

        user = q.first()
        if user:
            return self._mkuser(instance=user)

        return None
