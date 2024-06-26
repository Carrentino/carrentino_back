from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet

app_name = 'orders'

router_v1 = DefaultRouter()
router_v1.register(r'order', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router_v1.urls))
]