from rest_framework import serializers

from .model_serializers import UserSerializer


class AuthTokenSerializer(serializers.Serializer):
    '''Serializer for Login'''
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class AuthTokenOutputSerializer(serializers.Serializer):
    '''Serializer for output login'''
    refresh = serializers.CharField(required=True)
    access = serializers.CharField(required=True)
    user = UserSerializer()


class SendPasswordCodeSerializer(serializers.Serializer):
    '''Serializer for sending password code'''
    email = serializers.EmailField(required=True)


class VerifyCodeSerializer(serializers.Serializer):
    '''Serializer for verifying code'''
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)


class UpdatePasswordSerializer(serializers.Serializer):
    '''Serializer for updating password'''
    email = serializers.EmailField(required=True)
    new_password = serializers.CharField(required=True)
    code = serializers.CharField(required=True)
