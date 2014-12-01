""" External urls. """

from django.conf.urls import patterns, url

urlpatterns = patterns('external.views',
                       url(r'^$', 'index', name='index'),
                       url(r'^sponsorship$', 'sponsorship',
                           name='sponsorship'),
                       url(r'^about$', 'about',
                           name='about'),
                       )
