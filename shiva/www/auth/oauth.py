# -*- coding: utf-8 -*-
from shiva.www import app
from shiva.www.auth.models import User, OAuth

from flask import request, flash, redirect, session, g
from flaskext.oauth import OAuth as OAuthRegistry


oauth = OAuthRegistry()
twitter = oauth.remote_app('twitter',
    base_url='http://api.twitter.com/1/',
    request_token_url='http://api.twitter.com/oauth/request_token',
    access_token_url='http://api.twitter.com/oauth/access_token',
    authorize_url='http://api.twitter.com/oauth/authenticate',
    consumer_key=app.config['TWITTER_CONSUMER_KEY'],
    consumer_secret=app.config['TWITTER_CONSUMER_SECRET'],
)
facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=app.config['FACEBOOK_APP_ID'],
    consumer_secret=app.config['FACEBOOK_APP_SECRET'],
    request_token_params={'scope': 'email'},
)


def get_remote_app(app_name):
    if app_name == 'twitter':
        return twitter
    elif app_name == 'facebook':
        return facebook


@twitter.tokengetter
def get_twitter_token():
    """This is used by the API to look for the auth token and secret
    it should use for API calls.  During the authorization handshake
    a temporary set of token and secret is used, but afterwards this
    function has to return the token and secret.  If you don't want
    to store this in the database, consider putting it into the
    session instead.
    """
    if g.identity is not None:
        return (g.identity.oauth_token, g.identity.oauth_secret)


@twitter.authorized_handler
def twitter_authorized(response):
    """Called after authorization.  After this function finished handling,
    the OAuth information is removed from the session again.  When this
    happened, the tokengetter from above is used to retrieve the oauth
    token and secret.

    Because the remote application could have re-authorized the application
    it is necessary to update the values in the database.

    If the application redirected back after denying, the response passed
    to the function will be `None`.  Otherwise a dictionary with the values
    the application submitted.  Note that Twitter itself does not really
    redirect back unless the user clicks on the application name.
    """
    next_url = request.args.get('next') or url_for('index')
    if response is None:
        flash(u'You denied the request to sign in.', 'error')
        return redirect(next_url)

    name = response['screen_name']
    identity = OAuth.query.filter_by(service='twitter',
                                     identifier=name).first()
    if not identity:
        user = User()
        identity = OAuth(user=user, service='twitter', identifier=name,
                         oauth_token=response['oauth_token'],
                         oauth_secret=response['oauth_token_secret'])
        g.db.add(user)
    else:
        user = identity.user
        identity.oauth_token = response['oauth_token']
        identity.oauth_secret = response['oauth_token_secret']

    g.db.add(identity)
    g.db.commit()

    session['user_pk'] = user.pk
    flash('You were signed in')

    return redirect(next_url)


@facebook.authorized_handler
def facebook_authorized(response):
    next_url = request.args.get('next') or url_for('index')
    if response is None:
        flash('Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        ), 'error')
        return redirect(next_url)

    me = facebook.get('/me')
    fb_id = me.data['id']
    name = me.data['name']
    email = me.data['email']
    identity = OAuth.query.filter_by(service='facebook',
                                     identifier=fb_id).first()
    if not identity:
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(name=name, email=email)
            g.db.add(user)
        identity = OAuth(user=user, service='facebook', identifier=fb_id,
                         oauth_token=response['access_token'], oauth_secret='')
    else:
        user = identity.user
        identity.oauth_token = response['oauth_token']
        identity.oauth_secret = ''

    g.db.add(identity)
    g.db.commit()

    session['user_pk'] = user.pk
    flash('You were signed in')

    return redirect(next_url)


@facebook.tokengetter
def get_facebook_oauth_token():
    if g.identity is not None:
        return (g.identity.oauth_token, g.identity.oauth_secret)


def login_oauth(request):
    """
    """

    raise NotImplementedError
