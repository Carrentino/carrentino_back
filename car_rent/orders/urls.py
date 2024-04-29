from rest_framework.routers import DefaultRouter

from .views import OrderViewSet

router_v1 = DefaultRouter()
router_v1.register(r'order', OrderViewSet, basename='order')

urlpatterns = [

] + router_v1.urls