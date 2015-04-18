# encoding: utf-8
import logging
import sys
import json

from django.db import models
from django.conf import settings

class MutableModel(models.Model):
    # automatic metadata
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created']

# A device (optionally connected to a user) that we can send push notifications to
class PushDevice(MutableModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Owner of this device", null=True, blank=True)
    token = models.CharField("Device token string", max_length=255, db_index=True)
    
    def __unicode__(self):
        if self.user:
            return u"PushDevice %s connected to user: %s" % (self.token, self.user.username)
        else:
            return u"PushDevice %s" % self.token
        
    class Meta:
        unique_together = ('user', 'token')

# A push notification message.
class DelayedPushNotification(MutableModel):
    # to which user?
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True, null=True, blank=True)

    # ... or to which devices?
    to_device = models.ForeignKey(PushDevice, null=True, blank=True)
    
    # payload
    alert = models.CharField(blank=True, null=True, max_length=255)
    sound = models.CharField(blank=True, null=True, max_length=100)
    info_json = models.CharField(blank=True, null=True, max_length=512)

    def get_info(self):
        if self.info_json:
            return json.loads(self.info_json)
    def set_info(self, data):
        self.info_json = json.dumps(data)

    info = property(get_info, set_info)

    # sent status
    sent = models.BooleanField(default=False, db_index=True)
    num_tries = models.IntegerField(default=0)
    error = models.CharField(blank=True, max_length=255)
    expired = models.BooleanField(default=False)

    def deliver(self):
        # included here to avoid circular import
        from communication import notify_user, notify_devices

        success = False
        try:
            if self.to_user:
                # try to deliver to a device connected to a django user model
                logging.info("trying to deliver delayed push notification ID %d to %s", self.id, self.to_user.username)
                success = notify_user(self.to_user, alert=self.alert, sound=self.sound, info=self.info)
            else:
                # try to deliver to 'anonymous' device
                logging.info("trying to deliver delayed push notification ID %d to anonymous user", self.id)
                success = notify_devices(devices=[self.to_device], alert=self.alert, sound=self.sound, info=self.info)
        except:
            self.error = sys.exc_info()
            logging.error(sys.exc_info())
        finally:
            self.num_tries += 1
            
            if success:
                logging.info("sent successfully (try %d)!", self.num_tries)
                self.sent = True
            else:
                # expire after 5 unsuccessful delivery attempts
                if self.num_tries > 5:
                    self.expired = True
                
            self.save()
            
    class Meta:
        verbose_name = "Push notification"
        verbose_name_plural = "Push notifications"
