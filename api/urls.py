from django.urls import path
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('api/', views.fetch_and_store_vulnerabilities, name='fetch_and_store_vulnerabilities'),
    path('api/get/', views.get_all_vulnerabilities, name='get_all_vulnerabilities'),
    path('api/fixed/', views.mark_vulnerabilities_fixed, name='mark_vulnerabilities_fixed'),
    path('api/filtered/', views.get_unfixed_vulnerabilities, name='get_unfixed_vulnerabilities'),
    path('api/summary/', views.get_vulnerabilities_summary_by_severity, name='get_vulnerabilities_summary_by_severity'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]