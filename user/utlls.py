from typing import Any, Dict
from user.serializers import UserFollowListSerializer
from django.conf import settings
from functools import wraps
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail

from .models import UserModel

import jwt

KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'


def authorized(function):
    @wraps(function)
    def wrap(request: Request, *args, **kwargs):
        try:
            token = str(request.META['HTTP_AUTHORIZATION'])[7:]
            verified = jwt.decode(token, key=KEY, algorithms=ALGORITHM)
            user: UserModel = UserModel.objects.get(id=verified['id'])
            serialized = UserFollowListSerializer(user.follows, many=True)
            request.user = user
            request.follows = serialized.data
            return function(request, *args, **kwargs)
        except:
            return Response("Not authorized", status=status.HTTP_401_UNAUTHORIZED)
    return wrap


def generateToken(payload: Dict[str, Any]):
    return jwt.encode(payload, key=KEY, algorithm=ALGORITHM)
