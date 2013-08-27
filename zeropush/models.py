from django.db import models
from django.conf import settings

class PushDevice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Owner of this device")
    token = models.CharField("Device token string", max_length=255, db_index=True)
    
    def __unicode__(self):
        return u"UserDevice %s" % self.token
