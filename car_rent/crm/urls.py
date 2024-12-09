from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

app_name = 'crm'

router_v1 = DefaultRouter()

router_v1.register('cars', CompanyCarView, basename='cars')
router_v1.register('orders', CompanyOrderView, basename='orders')


urlpatterns = [
    path('v1/', include(router_v1.urls))
]
