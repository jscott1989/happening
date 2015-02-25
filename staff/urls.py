""" Member urls. """

from django.conf.urls import patterns, url

urlpatterns = patterns('staff.views',
                       url(r'^$', 'index', name='staff'),
                       url(r'^members$', 'members', name='staff_members'),
                       url(r'^members/(?P<pk>\d+)/staff$', 'make_staff',
                           name='make_staff'),
                       url(r'^members/(?P<pk>\d+)/not-staff$',
                           'make_not_staff', name='make_not_staff'),
                       url(r'^sponsors$', 'sponsors', name='staff_sponsors'),
                       url(r'^send_email$', 'send_email',
                           name='staff_send_email'),
                       url(r'^sponsors/create$', 'create_sponsor',
                           name='create_sponsor'),
                       url(r'^sponsors/(?P<pk>\d+)$', 'edit_sponsor',
                           name='edit_sponsor'),
                       url(r'^events$', 'events', name='staff_events'),
                       url(r'^events/create$', 'create_event',
                           name='create_event'),
                       url(r'^events/(?P<pk>\d+)$', 'edit_event',
                           name='edit_event'),
                       url(r'^events/(?P<pk>\d+)/vote_winner$',
                           'get_vote_winner', name='get_vote_winner'),
                       url(r'^events/(?P<pk>\d+)/email$', 'email_event',
                           name='email_event'),
                       )
