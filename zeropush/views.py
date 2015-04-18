# encoding: utf-8
import logging

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from models import PushDevice

@login_required
def add_user_device(request):
    token_string = request.POST.get("token", None)
    if token_string:
        device, created = PushDevice.objects.get_or_create(token=token_string, user=request.user)
        
        if created:
            # associate device with user
            logging.info("New device (%s) added for user %s" % (device.token, request.user))
            
        # success
        return HttpResponse(status=200)
    else:
        logging.error("Can't add user push device with empty token!")
        
        # bad request!
        return HttpResponse(status=400)

def add_anonymous_device(request):
    token_string = request.POST.get("token", None)
    if token_string:
        device, created = PushDevice.objects.get_or_create(token=token_string)
        
        if created:
            logging.info("New device (%s) added for anonymous user" % (device.token,))
            
        # success
        return HttpResponse(status=200)
    else:
        logging.error("Can't add push device with empty token!")
        
        # bad request!
        return HttpResponse(status=400)

