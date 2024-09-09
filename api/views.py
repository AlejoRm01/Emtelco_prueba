import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Vulnerability
from .serializers import VulnerabilitySerializer
import requests
from django.db.models import Count

logger = logging.getLogger('api')

@api_view(['GET'])
def fetch_and_store_vulnerabilities(request):
    logger.info('Fetching vulnerabilities from NVD')
    
    try:
        response = requests.get('https://services.nvd.nist.gov/rest/json/cves/2.0')
        response.raise_for_status()
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
        
        logger.info(f'{len(vulnerabilities)} vulnerabilities fetched and stored successfully')
        return Response({'message': 'Vulnerabilities fetched and stored successfully'})
    except requests.RequestException as e:
        logger.error(f'Error fetching vulnerabilities: {e}')
        return Response({'error': 'Failed to fetch vulnerabilities'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_all_vulnerabilities(request):
    logger.info('Fetching all vulnerabilities')
    vulnerabilities = Vulnerability.objects.all()
    serializer = VulnerabilitySerializer(vulnerabilities, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def mark_vulnerabilities_fixed(request):
    logger.info('Marking vulnerability as fixed')
    
    if not request.data or 'cve_id' not in request.data:
        logger.warning('Body is empty or missing cve_id')
        return Response(
            {'error': 'Body is empty or missing cve_id'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    cve_id = request.data.get('cve_id', None)
    
    if not cve_id:
        logger.warning('No CVE ID provided')
        return Response(
            {'error': 'No CVE ID provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    existing_vulnerability = Vulnerability.objects.filter(cve_id=cve_id).first()
    if not existing_vulnerability:
        logger.warning('No vulnerability found for the provided CVE ID')
        return Response(
            {'error': 'No vulnerability found for the provided CVE ID'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Mark the single vulnerability as fixed
    existing_vulnerability.fixed = True
    existing_vulnerability.save()
    logger.info(f'Vulnerability {cve_id} marked as fixed')
    
    return Response(
        {'message': 'Vulnerability fixed successfully'},
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def get_unfixed_vulnerabilities(request):
    logger.info('Fetching unfixed vulnerabilities')
    vulnerabilities = Vulnerability.objects.filter(fixed=False)
    serializer = VulnerabilitySerializer(vulnerabilities, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_vulnerabilities_summary_by_severity(request):
    logger.info('Fetching vulnerabilities summary by severity')
    summary = Vulnerability.objects.values('base_severity').annotate(count=Count('id'))
    return Response(summary)