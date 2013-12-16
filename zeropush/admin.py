from django.contrib import admin
from models import DelayedPushNotification, PushDevice

class DelayedPushNotificationAdmin(admin.ModelAdmin):
    list_display = ["created", "to_user", "alert", "num_tries", "sent"]
    readonly_fields = ["to_user", "alert", "sound", "sent", "num_tries", "error", "created", "expired", "info_json"]

class PushDeviceAdmin(admin.ModelAdmin):
    pass

admin.site.register(PushDevice, PushDeviceAdmin)
admin.site.register(DelayedPushNotification, DelayedPushNotificationAdmin)
