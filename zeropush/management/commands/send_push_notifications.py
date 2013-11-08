# encoding: utf-8
from django.core.management.base import NoArgsCommand, CommandError
from zeropush.models import DelayedPushNotification

class Command(NoArgsCommand):
    help = 'Sends all unsent push notifications'

    def handle_noargs(self, **options):
        unsent_pushes = DelayedPushNotification.objects.filter(sent=False, expired=False)
        for push in unsent_pushes:
            push.deliver()
        
