from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # POST API for adding a device with a token. requires the user to be logged in.
    url(r'^zeropush/add_device/$', 'zeropush.views.add_user_device'),
)