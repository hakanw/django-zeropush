# encoding: utf-8
import logging
import json
import requests

from django.conf import settings

ZEROPUSH_NOTIFY_URL = "https://api.zeropush.com/notify"

def notify_devices(devices, alert=None, sound=None, badge_number=None, info=None):
    if len(devices) > 0:
        params = {
            "auth_token": settings.ZEROPUSH_AUTH_TOKEN, 
            "device_tokens[]": [device.token for device in devices] 
        }
        if alert is not None:
            params.update({ "alert": alert })
        if sound is not None:
            params.update({ "sound": sound })
        if badge_number is not None:
            params.update({ "badge_number": badge_number })
        if info is not None:
            params.update({ "info": json.dumps(info) })
            
        response = requests.post(ZEROPUSH_NOTIFY_URL, params)
        if response.ok:
            logging.info("Push successfully sent to zeropush")
            return True
        else:
            logging.error("Error! Push failed to be sent to zeropush! Error response: %s" % response.text)
            return False
            
    return False

def notify_user(user, alert=None, sound=None, badge_number=None, info=None):
    return notify_devices(user.pushdevice_set.all(), alert=alert, sound=sound, badge_number=badge_number, info=info)
