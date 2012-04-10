# -*- coding: utf-8 -*-
from .models import db, User, OpenID, Identity
from .oauth import get_remote_app
from shiva.www import app

from flask import g, session
from flaskext.openid import OpenID as _OpenID
from flask import (abort, flash, g, redirect, render_template, request,
                   session, url_for)

oid = _OpenID(app)


@app.before_request
def before_request():
    g.db = db.session
    if not getattr(g, 'identity', None):
        g.identity = None
    if 'identity_pk' in session:
        g.identity = Identity.query.filter_by(pk=session['identity_pk']).one()
    if not getattr(g, 'user', None):
        g.user = None
    if 'user_pk' in session:
        g.user = User.query.filter_by(pk=session['user_pk']).one()


@app.after_request
def after_request(response):
    g.db.close()
    return response


def logout():
    session.pop('user_pk', None)
    flash(u'You have been signed out')
    return redirect(url_for('home'))


def get_next_url():
    return oid.get_next_url()


@oid.loginhandler
def login():
    """Logs the user in. It discovers the protocol needed for authentication
    and uses it transparently behind the scenes.
    """

    if g.user is not None:
        return redirect(oid.get_next_url())

    OPENID = 'OpenID'
    OAUTH = 'OAuth'
    auth_method = {
        'google': {'method': OPENID,
                   'url': 'https://www.google.com/accounts/o8/id'},
        'facebook': {'method': OAUTH},
        'twitter': {'method': OAUTH},
    }

    if request.method == 'POST':
        service = auth_method.get(request.form.get('loginusing'))
        if not service:
            abort(404)
        if service['method'] == OPENID:
            # Does the login via OpenID.  Has to call into `oid.try_login` to
            # start the OpenID machinery.
            return oid.try_login(service['url'],
                                 ask_for=['email', 'fullname', 'nickname'])
        if service['method'] == OAUTH:
            next_url = request.args.get('next') or request.referrer or None
            service_name = request.form.get('loginusing')
            callback = url_for('%s_authorized' % service_name, next=next_url)
            return get_remote_app(service_name).authorize(callback=callback)
    return redirect(url_for('home'))


@oid.after_login
def create_or_login(resp):
    """This is called when login with OpenID succeeded and it's not
    necessary to figure out if this is the users's first login or not.
    This function has to redirect otherwise the user will be presented
    with a terrible URL which we certainly don't want.
    """

    identity = OpenID.query.filter_by(identity_url=resp.identity_url).first()

    if identity is None:
        user = User(name=resp.fullname, email=resp.email)
        if user.email:
            user.active = True
        identity = OpenID(user=user, identity_url=resp.identity_url)

        g.db.add(user)
        g.db.add(identity)
        g.db.commit()
    else:
        user = identity.user

    g.user = user
    session['user_pk'] = user.pk
    flash(u'Successfully signed in')

    # return redirect(oid.get_next_url())
    return redirect(url_for('home'))


def signup():
    if request.method == 'POST':
        email = request.form['email']
    return render_template()


# TODO: A user can't do anything until the profile is complete. That is, name
# and (confirmed) e-mail.


# FIXME: Copy'n'pasted.
def profile():
    """If this is the user's first login, the create_or_login function
    will redirect here so that the user can set up his profile.
    """
    if g.user is not None or 'openid' not in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if not name:
            flash(u'Error: you have to provide a name')
        elif '@' not in email:
            flash(u'Error: you have to enter a valid email address')
        else:
            flash(u'Profile successfully created')
            db.add(User(name, email, session['openid']))
            db.commit()
            return redirect(oid.get_next_url())
    return render_template('create_profile.html', next_url=oid.get_next_url())


# FIXME: Copy'n'pasted.
def edit_profile():
    """Updates a profile"""
    if g.user is None:
        abort(401)
    form = dict(name=g.user.name, email=g.user.email)
    if request.method == 'POST':
        if 'delete' in request.form:
            db.delete(g.user)
            db.commit()
            session['openid'] = None
            flash(u'Profile deleted')
            return redirect(url_for('home'))
        form['name'] = request.form['name']
        form['email'] = request.form['email']
        if not form['name']:
            flash(u'Error: you have to provide a name')
        elif '@' not in form['email']:
            flash(u'Error: you have to enter a valid email address')
        else:
            flash(u'Profile successfully created')
            g.user.name = form['name']
            g.user.email = form['email']
            db.commit()
            return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html', form=form)


def recover():
    """
    """

    raise NotImplementedError
