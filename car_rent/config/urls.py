from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from orders.urls import router_v1

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users-api/', include("users.urls")),
    path('cars-api/', include("cars.urls")),
    path('orders-api/', include("orders.urls")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]
