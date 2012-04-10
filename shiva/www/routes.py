# -*- coding: utf-8 -*-
from shiva.www.auth.routes import *
from shiva.www import app
from shiva.www import views

url = app.add_url_rule

url('/', 'home', views.home)

url('/artist/<int:pk>/', 'artist', views.artist)
url('/song/<int:pk>/', 'song', views.song)
url('/pic/<int:tag_pk>/', 'pic', views.pic)
url('/stream/<int:song_pk>/', 'stream', views.stream)
url('/download/', 'download', views.download, methods=['GET', 'POST'])
url('/download/<int:song_pk>/', 'download', views.download)
url('/upload/', 'upload', views.upload)
url('/about/', 'about', views.about)
url('/contact/', 'contact', views.contact)
