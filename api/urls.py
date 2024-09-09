from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VulnerabilityViewSet

router = DefaultRouter()
router.register(r'vulnerabilities', VulnerabilityViewSet, basename='vulnerability')

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('vulnerabilities.urls')),
]