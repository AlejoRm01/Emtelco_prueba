from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Vulnerability
from .serializers import VulnerabilitySerializer
import requests
from django.db.models import Count

@api_view(['GET'])
def fetch_and_store_vulnerabilities(request):
    response = requests.get('https://services.nvd.nist.gov/rest/json/cves/2.0')
    data = response.json()
    vulnerabilities = data.get('vulnerabilities', [])
    
    for vuln in vulnerabilities:
        cve_data = vuln.get('cve', {})
        cve_id = cve_data.get('id', '')
        description = next((desc['value'] for desc in cve_data.get('descriptions', []) if desc['lang'] == 'en'), '')
        published_date = cve_data.get('published', '').split('T')[0]
        last_modified = cve_data.get('lastModified', '').split('T')[0]
        severity = cve_data.get('metrics', {}).get('cvssMetricV2', [{}])[0].get('baseSeverity', '')

        Vulnerability.objects.update_or_create(
            cve_id=cve_id,
            defaults={
                'description': description,
                'published_date': published_date,
                'last_modified': last_modified,
                'base_severity': severity
            }
        )
    
    return Response({'message': 'Vulnerabilities fetched and stored successfully'})

@api_view(['GET'])
def get_all_vulnerabilities(request):
    vulnerabilities = Vulnerability.objects.all()
    serializer = VulnerabilitySerializer(vulnerabilities, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def mark_vulnerabilities_fixed(request):
    if not request.data or 'cve_ids' not in request.data:
        return Response(
            {'error': 'Body is empty or missing cve_ids'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    cve_ids = request.data.get('cve_ids', [])
    
    if not cve_ids:
        return Response(
            {'error': 'No CVE ID provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    existing_vulnerabilities = Vulnerability.objects.filter(cve_id__in=cve_ids)
    if not existing_vulnerabilities.exists():
        return Response(
            {'error': 'No vulnerabilities found for the provided CVE ID'},
            status=status.HTTP_404_NOT_FOUND
        )

    updated_count = Vulnerability.objects.filter(cve_id__in=cve_ids).update(fixed=True)
    
    return Response(
        {'message': ' Vulnerability fixed successfully'},
        status=status.HTTP_200_OK
    )
    
@api_view(['GET'])
def get_unfixed_vulnerabilities(request):
    vulnerabilities = Vulnerability.objects.filter(fixed=False)
    serializer = VulnerabilitySerializer(vulnerabilities, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_vulnerabilities_summary_by_severity(request):
    summary = Vulnerability.objects.values('base_severity').annotate(count=Count('id'))
    return Response(summary)