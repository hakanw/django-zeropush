# encoding: utf-8
import logging

from django.db import models
from django.conf import settings

log = logging.getLogger(__name__)

class MutableModel(models.Model):
    # automatic metadata
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created']

# A device connected to a user that we can send push notifications to
class PushDevice(MutableModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Owner of this device")
    token = models.CharField("Device token string", max_length=255, db_index=True)
    
    def __unicode__(self):
        return u"UserDevice %s: %s" % (self.token, user.username)
        
    class Meta:
        unique_together = ('user', 'token')

# A push notification message.
class DelayedPushNotification(MutableModel):
    # to which user?
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True)
    
    # payload
    alert = models.CharField(blank=True, null=True, max_length=255)
    sound = models.CharField(blank=True, null=True, max_length=100)
    info = models.CharField(blank=True, null=True, max_length=512)
    
    # sent status
    sent = models.BooleanField(default=False, db_index=True)
    num_tries = models.IntegerField(default=0)
    error = models.CharField(blank=True, max_length=255)
    expired = models.BooleanField(default=False)

    def deliver(self):
        success = False
        log.info("trying to deliver delayed push notification ID %d to %s", self.id, self.user.username)
        try:
            success = zeropush.notify_user(self.user, alert=self.alert, sound=self.sound, info=info)
        except:
            self.error = sys.exc_info()
            log.error(sys.exc_info())
        finally:
            self.num_tries += 1
            
            if success:
                log.info("sent successfully (try %d)!", self.num_tries)
                self.sent = True
            else:
                # expire after 5 unsuccessful delivery attempts
                if self.num_tries > 5:
                    self.expired = True
                
            self.save()
            
    class Meta:
        verbose_name = "Push notification"
        verbose_name_plural = "Push notifications"
