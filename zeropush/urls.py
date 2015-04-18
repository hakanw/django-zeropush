# encoding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # user-oriented mode: attach the POSTed device token (PushDevice object) to the currently logged in user.
    # remember to include session token, CSRF token and all that jazz for this to work.
    url(r'^zeropush/add_current_user_device/$', 'zeropush.views.add_user_device'),

    # userless mode: add a device token (PushDevice object) to send notifications to.
    # remember to include CSRF token, if you have CSRF middleware turned on in your settings.
    # no need to be logged in to use this POST API.
    url(r'^zeropush/add_anonymous_device/$', 'zeropush.views.add_anonymous_device'),

    # deprecated URL, please use one of the options above.
   	url(r'^zeropush/add_device/$', 'zeropush.views.add_user_device'),
)