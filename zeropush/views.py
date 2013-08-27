# encoding: utf-8
import logging

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from models import PushDevice

log = logging.getLogger(__name__)

@login_required
def add_user_device(request):
    token_string = request.POST.get("token", None)
    if token_string:
        device, created = PushDevice.objects.get_or_create(token=token_string, user=request.user)
        
        if created:
            # associate device with user
            log.info("New device (%s) added for user %s" % (device.token, request.user))
            
        # success
        return HttpResponse(status=200)
    else:
        log.error("Can't add user push device with empty token!")
        
        # bad request!
        return HttpResponse(status=400)