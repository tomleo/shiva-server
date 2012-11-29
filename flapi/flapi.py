# -*- coding: utf-8 -*-
from flask import Flask, json, Response, url_for
from models import Audio, session


# configuration
DEBUG = True

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLAPI_SETTINGS', silent=True)


def gentestsdata():
    # audio1 = Audio(artist='artist1', title='title1', path='/path/to/audio1')
    # audio2 = Audio(artist='artist2', title='title2', path='/path/to/audio2')
    # session.add_all([audio1, audio2])
    # session.commit()

    return None


def path_to_url(path):
    return path


def mk_song(audio):
    return {
        'id': audio.pk,
        'uri': 'http://localhost:5000%s' % url_for('.song', song_id=audio.pk),
        'artist': audio.artist,
        'title': audio.title,
        'stream_uri': audio.path,
    }


def mk_response(body):
    mime = 'application/json'

    return Response(response=json.dumps(body), mimetype=mime,
                    content_type=mime)


@app.route('/songs/')
def songs():
    response = []
    for audio in session.query(Audio).all():
        response.append(mk_song(audio))

    return mk_response(response)


@app.route('/song/<int:song_id>/')
def song(song_id):
    audio = session.query(Audio).get(song_id)

    return mk_response(mk_song(audio))


if __name__ == '__main__':
    app.run()
