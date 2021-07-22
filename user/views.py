from typing import List
from django.core.exceptions import ValidationError
from rest_framework.parsers import FileUploadParser
from user.utlls import authorized, generateToken
from django.conf import settings
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status
import cloudinary
import cloudinary.uploader

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

from .models import UserModel
from .serializers import UserFollowListSerializer, UserListSerializer, UserCreateSerializer, UserLoginSerializer

@api_view(['GET'])
@authorized
def list(_):
    """Get list of records of all users"""
    all = UserModel.objects.all()
    serialized = UserListSerializer(all, many=True)
    return Response({"users": serialized.data}, status=200)

@api_view(['GET'])
@authorized
def listOne(_, id=None):
    """Get record of a specific user"""
    try:
        all = UserModel.objects.get(id=id)
        serialized = UserListSerializer(all, many=False)
        return Response({"user": serialized.data}, status=200)
    except:
        return Response({"user": None}, status=200)

@api_view(['POST'])
def create(request: Request):
    """Register a new user"""
    serialized = UserCreateSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        return Response({"message": "user created successfully"}, status=200)
    else:
        return Response({"message": "Validation error", "data": serialized.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['POST'])
def login(request: Request):
    """Check login for an existing new user"""
    print(request.data)
    login_serialized = UserLoginSerializer(data=request.data)
    if not login_serialized.is_valid():
        return Response({"error": login_serialized.errors}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        user = UserModel.objects.get(email=login_serialized.data['email'])
        if not user.password == login_serialized.data['password']:
            return Response({"message": "Credentials didn't match."}, status=status.HTTP_401_UNAUTHORIZED)
        # login successful
        user_data = UserListSerializer(user, many=False)
        access_token = generateToken(user_data.data)
        return Response({"message": "Login successful.", "token": access_token}, status=status.HTTP_200_OK)
    except:
        return Response({"message": "Account not found."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['GET'])
@authorized
def refreshToken(request):
    try:
        user = request.user
        user_data = UserListSerializer(user, many=False)
        access_token = generateToken(user_data.data)
        return Response({"token": access_token}, status=status.HTTP_200_OK)
    except:
        return Response({"message": "Could not refresh token."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@authorized
def followUser(request: Request):
    try:
        toFollow = request.data['id']

        if toFollow == request.user.id:
            return Response({"message": "Cannot follow yourself."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)    
        userToFollow = UserModel.objects.get(id=toFollow)
        user : UserModel = request.user
        user.follows.add(userToFollow)
        return Response({"message": "User follow successful."}, status=status.HTTP_200_OK)
    except:
        return Response({"message": "Something went wrong."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['GET'])
@authorized
def getFollows(request: Request):
    try:
        user : UserModel = request.user
        follows: List[UserModel] = user.follows.all()
        serialized = UserFollowListSerializer(follows, many=True)
        return Response({"follows": [serialized.data]}, status=status.HTTP_200_OK)
    except:
        return Response({"message": "Something went wrong."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['PUT'])
@parser_classes([FileUploadParser])
@authorized
def image_upload(request: Request, filename: str):
    '''Upload image for post'''
    try:
        file_obj = request.data['file']
        photo = cloudinary.uploader.upload_image(file_obj, folder="users/" + request.user.name)
        user : UserModel = request.user
        user.image = photo.build_url()
        user.save()
        return Response({"message": "Uploaded successfully", "image": user.image})
    except:
        return Response({"message": "Upload failed."}, status=500)