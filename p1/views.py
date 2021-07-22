from django.conf import settings
from django.http import HttpResponse
from rest_framework.decorators import api_view

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

@api_view(['GET'])
def welcome_view(_, *args, **kw):
    return HttpResponse("Welcome to test P1", status=200)