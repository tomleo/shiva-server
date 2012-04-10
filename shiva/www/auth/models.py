# -*- coding: utf-8 -*-
from shiva.www import app

from flaskext.sqlalchemy import SQLAlchemy
from hashlib import sha512
import os

db = SQLAlchemy(app)


class User(db.Model):
    """
    """

    __tablename__ = 'users'

    pk = db.Column(db.Integer, db.Sequence('user_pk'), primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(256), unique=True)
    active = db.Column(db.Boolean)

    identities = db.relationship('Identity', backref='user', lazy='dynamic')

    def __repr__(self):
        return self.email


class Identity(db.Model):
    """
    """

    __tablename__ = 'identities'

    pk = db.Column(db.Integer, db.Sequence('identity_pk'), primary_key=True)
    auth_method = db.Column(db.String(32), nullable=False)

    user_pk = db.Column(db.Integer, db.ForeignKey('users.pk'))

    __mapper_args__ = {'polymorphic_on': auth_method}


class OpenID(Identity):
    """
    """

    __tablename__ = 'openid'

    identity_url = db.Column(db.String(256))
    identity_pk = db.Column(None, db.ForeignKey('identities.pk'),
                            primary_key=True)

    __mapper_args__ = {'polymorphic_identity': 'openid'}


class OAuth(Identity):
    """
    """

    __tablename__ = 'oauth'

    service = db.Column(db.String(32))
    identifier = db.Column(db.String(64))
    oauth_token = db.Column(db.String(128))
    oauth_secret = db.Column(db.String(128))

    identity_pk = db.Column(None, db.ForeignKey('identities.pk'),
                            primary_key=True)

    __mapper_args__ = {'polymorphic_identity': 'oauth'}


class Local(Identity):
    """
    """

    __tablename__ = 'local'

    password = db.Column(db.String(128), nullable=True)
    identity_pk = db.Column(None, db.ForeignKey('identities.pk'),
                            primary_key=True)

    __mapper_args__ = {'polymorphic_identity': 'local'}

    def set_password(self, raw_password):
        """Sets the password for a user.
        """

        hash_this = '%s$#$%s' % (raw_password, app.config.SECRET_KEY)
        self.password = sha512(hash_this).hexdigest()
