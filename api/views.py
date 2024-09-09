from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Vulnerability
from .serializers import VulnerabilitySerializer

class VulnerabilityViewSet(viewsets.ViewSet):
    
    def list(self, request):
        queryset = Vulnerability.objects.all()
        serializer = VulnerabilitySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        cve_ids = request.data.get('cve_ids', [])
        Vulnerability.objects.filter(cve_id__in=cve_ids).update(fixed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def retrieve(self, request, pk=None):
        queryset = Vulnerability.objects.all()
        if pk:
            queryset = queryset.filter(cve_id=pk)
        serializer = VulnerabilitySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_fixed_vulnerabilities(self):
        queryset = Vulnerability.objects.filter(fixed=True)
        serializer = VulnerabilitySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_vulnerabilities_by_severity(self):
        vulnerabilities = Vulnerability.objects.values('severity').annotate(count=models.Count('id'))
        return Response(vulnerabilities)