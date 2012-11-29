# -*- coding: utf-8 -*-
from flask import jsonify
from models import Audio


class BaseResource(object):
    def all(self):
        raise NotImplementedError

    def as_dict(self):
        raise NotImplementedError

    def make_response(self):
        from flask import Response

        mime = 'application/json'
        response = Response(mimetype=mime, content_type=mime)
        response.response = jsonify(self.as_dict)

        return response


class Song(BaseResource):
    def __init__(self, pk):
        self.pk = pk

    def all(self):
        return Audio.query.all()

    def get_instance(self):
        from models import Audio

        return Audio.query.get(self.pk)

    def as_dict(self):
        inst = self.get_instance()
        return inst
