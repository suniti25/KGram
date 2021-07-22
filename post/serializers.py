from rest_framework import serializers

from user.models import UserModel

from .models import CommentModel, PostLikeModel, PostModel

POST_CONTENT_THRESHOLD = 240

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = "__all__"
        depth = 1


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ["content", "image"]
    
    def validate(self, value):
        content = value['content']
        if len(content) > POST_CONTENT_THRESHOLD:
            raise serializers.ValidationError("Content is too long.")
        return value

class PostLikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikeModel
        fields = ['post']


class PostLikeListOfUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikeModel
        fields = ['liked_by']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['comment', 'post']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = '__all__'
        depth = 1
