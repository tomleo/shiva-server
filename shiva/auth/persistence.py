# -*- coding: utf-8 -*-
import os
from hashlib import sha512
from sqlalchemy import (Boolean, Column, ForeignKey, Integer, Sequence,
                        String,)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .config import config


Base = declarative_base()


class User(Base):
    """
    """

    __tablename__ = 'users'

    pk = Column(Integer, Sequence('user_pk'), primary_key=True)
    name = Column(String(64), nullable=True)
    email = Column(String(256), unique=True)
    password = Column(String(256))
    active = Column(Boolean)

    # identities = relationship('Identity', backref='user', lazy='dynamic')

    def __repr__(self):
        return self.email

    @staticmethod
    def hash_password(raw_password):
        """Hashes a password.
        """

        hash_this = '%s$#$%s' % (raw_password, config['SECRET_KEY'])

        return sha512(hash_this).hexdigest()

    def set_password(self, raw_password):
        """Sets the password for a user.
        """

        self.password = self.__class__.hash_password(raw_password)
