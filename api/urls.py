from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.fetch_and_store_vulnerabilities),
    path('api/get/', views.get_all_vulnerabilities),
    path('api/fixed/', views.mark_vulnerabilities_fixed),
    path('api/filtered/', views.get_unfixed_vulnerabilities),
    path('api/summary/', views.get_vulnerabilities_summary_by_severity),
]