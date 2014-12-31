""" Member urls. """

from django.conf.urls import patterns, url

urlpatterns = patterns('members.views',
                       url(r'^(?P<pk>\d+)/settings$', 'settings',
                           name='settings'),
                       url(r'^(?P<pk>\d+)/settings/username$', 'edit_username',
                           name='edit_username'),
                       url(r'^(?P<pk>\d+)$', 'view_profile',
                           name='view_profile'),
                       url(r'^(?P<pk>\d+)/edit$', 'edit_profile',
                           name='edit_profile'),
                       url(r'^(?P<pk>\d+)/edit/photo$', 'upload_profile_photo',
                           name='upload_profile_photo'),
                       url(r'^(?P<pk>\d+)/edit/photo/crop$',
                           'resize_crop_profile_photo',
                           name='resize_crop_profile_photo'),
                       url(r'^tickets$', 'my_tickets',
                           name='my_tickets'),
                       url(r'^tickets/(?P<pk>\d+)$', 'edit_ticket',
                           name='edit_ticket'),
                       url(r'^tickets/(?P<pk>\d+)/cancel$', 'cancel_ticket',
                           name='cancel_ticket'),
                       )
