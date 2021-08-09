from rest_framework import serializers
from random import randint
from .models import UserModel
from smtplib import SMTPException
from django.conf import settings
from django.core.mail import send_mail

EMAIL_SUFFIX = ['@ku.edu.np', '@student.ku.edu.np']


def sendEmail(email_to: str = None, email_body: str = None):
    email_subject = 'Activation'
    return send_mail(
        email_subject,
        email_body,
        settings.EMAIL_HOST_USER,
        [email_to],
        fail_silently=False
    )


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'name', 'image', 'follows', 'otp']


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

    def save(self, **kwargs):
        try:
            print(self.validated_data)
            otp = randint(100000, 999999)
            email_body = str(otp) + ' enter this'
            sendEmail(
                self.validated_data['email'],
                email_body,
            )
            record = super().save(otp=otp, **kwargs)
            return record
        except SMTPException as x:
            print(x)
            raise x


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
