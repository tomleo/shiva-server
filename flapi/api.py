# -*- coding: utf-8 -*-
"""
cat /dev/brain
==============

Just a series of thoughts about how the Flask-Restless' API could be like. None
of this has been through any serious thought about fesibility, this are just
random ideas.
"""
from flask.ext.restless import APIManager, Resource
from flapi.models import session, Audio


class SongResource(Resource):
    """
    This approach is based on
    https://code.google.com/p/django-rest-interface/wiki/RestifyDjango
    and
    http://django-tastypie.readthedocs.org/en/latest/resources.html
    """

    def create(self):
        pass

    def read(self, id=None):
        pass

    def update(self, *args, **kwargs):
        pass

    def delete(self, id):
        pass

    def patch(self):
        pass

    def head(self):
        pass

    def options(self):
        pass

    def connect(self):
        raise NotImplementedError

    def trace(self):
        raise NotImplementedError

    def validator(self, data):
        """
        Validates the data sent by the client. Run always before every method.
        Maybe could be turn into a decorator (like before_request)
        """
        pass


# --


class SongResource(Resource):
    """
    A less django-ish approach.
    """

    # A more SQLAlchemy-ish approach.
    __basemodel__ = Audio

    # This method decorator should be defined once and only once per Verb. It
    # would tell the Resource how to read/write. Me gusta.
    @method('GET')
    def get_all_or_one(self, id=None):
        pass

    @method(['POST', 'PUT', 'PATCH'])
    def write(self, data):
        pass


# --


# Registering the Route. For both previous examples.
# Maybe decorate the class? /me not likes
@app.route('/songs/')
class SongResource(Resource):
    pass


# Use the add_url_rule decorator.
app.add_url_rule('/songs/', 'songs', SongResource)

# Downside: Duplication.
app.add_url_rule('/songs/<int:song_id>', 'song', SongResource)

# Possible solution, delegate to the Resource?
SongResource.create_rules(app)


# --


# This is a more flasky approach. Simple, extensible.
# ME GUSTA
api = APIManager(app, session=session)

@api.resource('/songs')
def songs(song_id=None):
    pass

# Note that the decorator now is the previous function.
@songs.method('PUT')
def save_song(data):
    pass

# The problem I see with this is how to build a resource from existing models
# using this approach. Doesn't look very straightforward at first.
# Maybe...
api.resource(Audio, methods=['GET', 'POST', 'DELETE'])


# --


# The present way:
manager = APIManager(app, session=session)
# Not a big fan of the 'create_api' method name.
manager.create_api(Audio, methods=['GET', 'POST', 'DELETE'])


# --


"""
Unsolved issues
---------------

* Define nested resources.
    * Serializers?
* Permissions for nested resources.
* Depth of nested resources.
* Definition of formats to retrieve.

Ideas:
* https://github.com/tryolabs/django-tastypie-extendedmodelresource#readme
* http://django-rest-framework.org/tutorial/1-serialization.html
* http://django-rest-framework.org/api-guide/serializers.html

"""

# :wq
