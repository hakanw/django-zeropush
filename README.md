django-zeropush
===============

A django app that helps you use [ZeroPush](http://zeropush.com)'s push notification API simply in your django backend for a Android or iOS app.

# django-zeropush features

1. a simple HTTP POST interface for adding new push devices connected to the current django user session
2. easy to use methods for sending push notifications to a user's all devices /or/ a group of specific devices
3. a PushDevice model that is connected to django's built-in user model (and also works with django 1.5+ custom user models)

# Example code

## Sending a notification to a user
```python
import zeropush

# Get a user. Can also be a custom user model in django 1.5+
the_user = User.objects.filter(username="johndoe")

zeropush.notify_user(the_user, alert="Here's some notification text", sound="default", badge_number=1)
```

## Getting all users' push devices and sending a notification to all of them
```python
from zeropush.models import PushDevice

# PushDevice is a model in django-zeropush that has a device token (string) and is connected to a django user.
all_devices = PushDevice.objects.all()

zeropush.notify_devices(all_devices, alert="Here's some text to all users")
```

# Installation

1. Add `zeropush` to your `INSTALLED_APPS` in your project's `settings.py`
2. Include `zeropush.urls` to your `urls.py` if you want a HTTP POST API for adding a push device token to a logged in user. See below for how to POST to it.
3. Run `./manage.py syncdb` to create the PushDevice model's table.
4. Now you can send push notifications as above!

# The HTTP API for adding new push tokens

Once you've added `zeropush.urls` to your `urls.py` file, a logged in user session can POST to `/zeropush/add_device/` with a parameter `token` which is the device token string to a new `PushDevice` object that associates the current django user with a specific device token.



