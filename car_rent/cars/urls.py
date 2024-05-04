from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

app_name = 'cars'

router_v1 = DefaultRouter()

router_v1.register('brand', BrandView, basename='brand')
router_v1.register('car-model', CarModelView, basename='car-model')
router_v1.register('car', CarView, basename='car')
router_v1.register('car-photo', CarPhotoView, basename='car-photo')
router_v1.register('car-option', CarOptionView, basename='car-option')


urlpatterns = [
    path('v1/', include(router_v1.urls))
]
