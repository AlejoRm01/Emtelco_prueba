from django.urls import path
from django.urls import re_path
from rest_framework import permissions
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('api/', views.fetch_and_store_vulnerabilities, name='fetch_and_store_vulnerabilities'),
    path('api/get/', views.get_all_vulnerabilities, name='get_all_vulnerabilities'),
    path('api/fixed/', views.mark_vulnerabilities_fixed, name='mark_vulnerabilities_fixed'),
    path('api/filtered/', views.get_unfixed_vulnerabilities, name='get_unfixed_vulnerabilities'),
    path('api/summary/', views.get_vulnerabilities_summary_by_severity, name='get_vulnerabilities_summary_by_severity'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)