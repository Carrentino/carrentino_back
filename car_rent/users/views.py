from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from .serializers.model_serializers import (UserRegisterSerializer,
                                            UserSerializer)
from .serializers.serializers import (AuthTokenOutputSerializer,
                                      AuthTokenSerializer,
                                      SendPasswordCodeSerializer,
                                      UpdatePasswordSerializer,
                                      VerifyCodeSerializer)
from .tasks import send_password_change_email
from .utils import authenticate_user, generate_code, update_password

User = get_user_model()


class RegistrationView(APIView):
    '''Registration'''

    @extend_schema(
        request=UserRegisterSerializer,
        responses={
            status.HTTP_201_CREATED: UserRegisterSerializer,
            status.HTTP_400_BAD_REQUEST: {
                "type": "object",
                "properties": {
                    "email": {"type": "array", "items": {"type": "string"}},
                    "first_name": {"type": "array", "items": {"type": "string"}},
                    "last_name": {"type": "array", "items": {"type": "string"}},
                    "password": {"type": "array", "items": {"type": "string"}}
                },
                "example": {
                    "email": ["This field is required."],
                    "first_name": ["This field is required."],
                    "last_name": ["This field is required."],
                    "password": ["This field is required."]
                }
            }
        },
        description='Endpoint for user registration'
    )
    def post(self, request):
        user_data = request.data.copy()
        serializer = UserRegisterSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomObtainAuthToken(TokenViewBase):
    '''Authorization'''
    @extend_schema(
        request=AuthTokenSerializer,
        responses={
            status.HTTP_201_CREATED: AuthTokenOutputSerializer,
            status.HTTP_400_BAD_REQUEST: {
                "type": "object",
                "properties": {
                    "email": {"type": "array", "items": {"type": "string"}},
                    "password": {"type": "array", "items": {"type": "string"}}
                },
                "example": {
                    "email": ["This field is required."],
                    "password": ["This field is required."]
                }
            }
        },
        description='Endpoint for user login'
    )
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        email = validated_data.get('email')
        password = validated_data.get('password')

        user = authenticate_user(email, password)

        refresh = RefreshToken.for_user(user)
        token_serializer = AuthTokenOutputSerializer({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
        return Response(token_serializer.data, status=status.HTTP_202_ACCEPTED)


class SendPasswordCodeView(APIView):
    '''Send password code'''
    @extend_schema(
        request=SendPasswordCodeSerializer,
        responses={
            status.HTTP_202_ACCEPTED: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "detail": 'Message successfully sent',
                }
            },
        },
        description='Endpoint for updating user password'
    )
    def post(self, request):
        serializer = SendPasswordCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = get_object_or_404(User, email=email)
        first_name = user.first_name
        last_name = user.last_name
        code = generate_code()
        send_password_change_email.delay(email, code, first_name, last_name)
        cache.set(email, code, timeout=settings.CODE_LIFETIME)
        return Response({'detail': 'Message successfully sent'}, status=status.HTTP_202_ACCEPTED)


class VerifyCodeView(APIView):
    '''Verify password code'''
    @extend_schema(
        request=VerifyCodeSerializer,
        responses={
            status.HTTP_202_ACCEPTED: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "detail": 'Code is correct',
                }
            },
            status.HTTP_403_FORBIDDEN: {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                },
                "example": {
                    "error": 'Code is not correct',
                }
            },
        },
        description='Endpoint for verifying user code'
    )
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        code = serializer.validated_data.get('code')
        if code == cache.get(email):
            return Response({'detail': 'Code is correct'}, status=status.HTTP_202_ACCEPTED)
        return Response({'error': 'Code is not correct'}, status=status.HTTP_403_FORBIDDEN)


class UpdatePasswordView(APIView):
    '''Update Password'''

    @extend_schema(
        request=UpdatePasswordSerializer,
        responses={
            status.HTTP_200_OK: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "detail": 'Password successfully updated',
                }
            },
            status.HTTP_403_FORBIDDEN: {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                },
                "example": {
                    "error": 'Code is timeout',
                }
            },
        },
        description='Endpoint for updating user password'
    )
    def patch(self, request):
        serializer = UpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        code = serializer.validated_data.get('code')
        new_password = serializer.validated_data.get('new_password')
        if code == cache.get(email):
            update_password(email, new_password)
            cache.delete(email)
            return Response({'detail': 'Password successfully updated'}, status=status.HTTP_200_OK)
        return Response({'error': 'Code is timeout'}, status=status.HTTP_403_FORBIDDEN)
