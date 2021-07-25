from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, parser_classes
from rest_framework import settings, status
from rest_framework.parsers import FileUploadParser
import cloudinary
import cloudinary.uploader

import facebook

from user.utlls import authorized

from .models import CommentModel, PostLikeModel, PostModel
from .serializers import CommentCreateSerializer, CommentSerializer, PostLikeListOfUsersSerializer, PostListSerializer, PostCreateSerializer

facebookGraph = facebook.GraphAPI({"EAAFBg1UDY20BAOTOKWyzorjBcppQoq137tiJmX4j7ILgPQ6PfBZBblbmFq0bHasu57UlpKuIfLkkX03f9m5LbxpWIeOlmlvQmSrmQ0lSVJn1skq448X39D5W8FQbjCdLerhOk7MpXE9BQVLyjJgzyGRazS9jaM1TYzoICsiAeGED2D2I4V4ao7JvZAKpZA8qkHfZBjttowZDZD"})

@api_view(["GET"])
@authorized
def list(_):
    """Get list of all posts"""
    try:
        all = PostModel.objects.all()
        serialized = PostListSerializer(all, many=True)
        return Response({"posts" : serialized.data}, status=200)
    except:
        return Response({"posts" : []}, status=500)

@api_view(["GET"])
@authorized
def listOneById(_, id):
    """Get details of one post"""
    try:
        oneRecord = PostModel.objects.get(id=id)
        serialized = PostListSerializer(oneRecord, many=False)
        return Response({"post" : serialized.data}, status=200)
    except:
        return Response({"post" : None}, status=200)

@api_view(["GET"])
@authorized
def listOneByUser(_, user_id):
    """Get list of posts made by a user"""
    try:
        all = PostModel.objects.all().filter(posted_by=user_id)
        serialized = PostListSerializer(all, many=True)
        return Response({"posts" : serialized.data}, status=200)
    except:
        return Response({"posts" : []}, status=200)

@api_view(["GET"])
@authorized
def listOneByUserByEmail(_, email):
    """Get list of posts made by a email of a user"""
    try:
        all = PostModel.objects.all().filter(posted_by__email=email)
        serialized = PostListSerializer(all, many=True)
        return Response({"posts" : serialized.data}, status=200)
    except:
        return Response({"posts" : []}, status=200)

@api_view(["POST"])
@authorized
def create(request: Request):
    """Make a new post"""
    try:
        serialized = PostCreateSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save(posted_by=request.user)
            post = PostModel.objects.all().filter(posted_by=request.user)[:1]
            return Response({"message": "post created successfully", "id": post.get().id}, status=200)
        else:
            return Response({"message": "Validation error", "data": serialized.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
        return Response({}, 500)

@api_view(['GET'])
@authorized
def getFeed(request: Request):
    try:
        followList = [x['id'] for x in request.follows]
        feed = PostModel.objects.all().filter(posted_by__in=followList)[:20]
        serialized = PostListSerializer(feed, many=True)
        return Response({"posts" : serialized.data}, status=200)
    except:
        return Response({"error" : "No feed"}, status=404)


@api_view(['GET'])
@authorized
def getLikeCountByPost(_, post):
    '''Get count of likes on a specific post'''
    try:
        original_post = PostModel.objects.get(id=post)
        all = PostLikeModel.objects.all().filter(post=original_post)
        serialized = PostLikeListOfUsersSerializer(all, many=True)
        likedByUser = [(x['liked_by'] == _.user.id) for x in serialized.data]
        return Response({"likes": len(serialized.data), 'likedByUser': any(likedByUser)}, status=status.HTTP_200_OK)
    except:
        return Response({"likes": None}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authorized
def getLikesByPost(_, post):
    '''Get list of likes on a specific post'''
    try:
        original_post = PostModel.objects.get(id=post)
        all = PostLikeModel.objects.all().filter(post=original_post)
        serialized = PostLikeListOfUsersSerializer(all, many=True)
        list = [item['liked_by'] for item in serialized.data]
        return Response({"likes": list}, status=status.HTTP_200_OK)
    except:
        return Response({"likes": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@authorized
def postLike(request: Request):
    '''Like a certain post'''
    try:
        post_to_like = PostModel.objects.get(id=request.data['post'])
        user = request.user
        prev_like = PostLikeModel.objects.filter(post=post_to_like, liked_by=user)
        if not prev_like.exists():
            PostLikeModel.objects.create(liked_by=user, post=post_to_like)
        return Response({"like": "successful"}, status=status.HTTP_200_OK)
    except:
        return Response({"message": "Something went wrong"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['PUT'])
@parser_classes([FileUploadParser])
@authorized
def image_upload(request: Request, filename: str):
    '''Upload image for post'''
    try:
        file_obj = request.data['file']
        name = cloudinary.uploader.upload_image(file_obj, folder="posts/" + request.user.name)
        return Response({"message": "Uploaded successfully", "filename": name.build_url()})
    except:
        return Response({"message": "Upload failed."}, status=500)

@api_view(['GET'])
@authorized
def comment_detail(_, post):
    '''Get count of comments on a specific post'''
    all = CommentModel.objects.all().filter(post=post).count()
    return Response({"comment": all}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authorized
def create_comment(request: Request):
    '''create comment'''
    serialized = CommentCreateSerializer(data=request.data)
    try:
        if not serialized.is_valid():
            return Response({"message": "Validation error", "data": serialized.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        serialized.save(commented_by=request.user)
        return Response({"message": "Comment created successfully"}, status=200)
    except:
        return Response({"comment": []}, status=500)


@api_view(['GET'])
@authorized
def list_comment(_, post):
    try:
        comment_list = CommentModel.objects.all().filter(post=post)
        serialized = CommentSerializer(comment_list, many=True)
        return Response({"comments": serialized.data}, status=status.HTTP_200_OK)
    except:
        return Response({"comment": []}, status=500)
    
@api_view(['GET'])
@authorized
def getFacebookPosts(_):
    fields= ['id', 'message', 'picture', 'created_time']
    profile = facebookGraph.get_object('Leo.KU.kavre/feed',fields=','.join(fields))
    return Response(profile)
