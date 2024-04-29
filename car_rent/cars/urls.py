from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

app_name = 'cars'

router = DefaultRouter()

router.register('brands', BrandView, basename='brands')
router.register('car_models', CarModelView, basename='car_models')
router.register('car', CarView, basename='car')

urlpatterns = [
    path('', include(router.urls))
]
