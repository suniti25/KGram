from rest_framework import serializers

from .models import UserModel

EMAIL_SUFFIX=['@ku.edu.np', '@student.ku.edu.np']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'name', 'image', 'follows']

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"

    def validate(self, values):
        email = values['email']
        for esf in EMAIL_SUFFIX:
            if email[-len(esf):] == esf:
                return values
        raise serializers.ValidationError("Email is invalid.")

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate_email(self, value):
        if not len(value):
            raise serializers.ValidationError("Email is required.")
        return value

    def validate_password(self, value):
        if not len(value):
            raise serializers.ValidationError("Password is required.")
        return value


class UserFollowListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'name']