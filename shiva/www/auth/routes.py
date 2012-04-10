# -*- coding: utf-8 -*-
from shiva.www import app
from shiva.www.auth import views, oauth

url = app.add_url_rule

# url('/login/openid/', 'openid', views.login_openid, methods=['GET', 'POST'])
# url('/login/oauth/', 'oauth', views.oauth, methods=['GET', 'POST'])
url('/login/twitter/authorized/', 'twitter_authorized',
    oauth.twitter_authorized, methods=['GET', 'POST'])
url('/login/facebook/authorized/', 'facebook_authorized',
    oauth.facebook_authorized, methods=['GET', 'POST'])
url('/profile/', 'profile', views.profile, methods=['GET', 'POST'])
url('/login/', 'login', views.login, methods=['GET', 'POST'])
url('/logout/', 'logout', views.logout)
url('/signup/', 'signup', views.signup, methods=['POST'])
url('/recover/', 'recover', views.recover)
