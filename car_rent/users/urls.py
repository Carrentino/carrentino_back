from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

urlpatterns = [
    path('api/token/', CustomObtainAuthToken.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', RegistrationView.as_view(), name='token_registration'),
    path('send_code/', SendPasswordCodeView.as_view(), name='token_send_code'),
    path('verify_code/', VerifyCodeView.as_view(), name='token_verify_code'),
    path('update_password/', UpdatePasswordView.as_view(), name='update_password'),
]
