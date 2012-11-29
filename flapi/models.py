# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////tmp/flapi.db', echo=True)
Session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


class Audio(Base):
    __tablename__ = 'audios'

    pk = Column(Integer, primary_key=True)
    artist = Column(String(64))
    title = Column(String(64))
    path = Column(String(128))
    quality = Column(String(64))

Base.metadata.create_all(engine)

session = Session()
