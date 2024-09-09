from django.test import TestCase

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from .models import Vulnerability

class VulnerabilityTests(APITestCase):

    def setUp(self):
        self.vulnerability = Vulnerability.objects.create(
            cve_id="CVE-2024-12345",
            description="Test vulnerability",
            published_date="2024-01-01",
            last_modified="2024-01-02",
            base_severity="HIGH"
        )

    @patch('requests.get')
    def test_fetch_and_store_vulnerabilities(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'vulnerabilities': [
                {
                    'cve': {
                        'id': 'CVE-2024-12346',
                        'descriptions': [{'lang': 'en', 'value': 'Another test vulnerability'}],
                        'published': '2024-01-03T00:00:00.000',
                        'lastModified': '2024-01-04T00:00:00.000',
                        'metrics': {'cvssMetricV2': [{'baseSeverity': 'MEDIUM'}]}
                    }
                }
            ]
        }

        url = reverse('fetch_and_store_vulnerabilities')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Vulnerabilities fetched and stored successfully'})
        self.assertTrue(Vulnerability.objects.filter(cve_id='CVE-2024-12346').exists())

    def test_get_all_vulnerabilities(self):
        url = reverse('get_all_vulnerabilities') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_mark_vulnerabilities_fixed(self):
        url = reverse('mark_vulnerabilities_fixed')
        data = {'cve_id': 'CVE-2024-12345'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vulnerability.refresh_from_db()
        self.assertTrue(self.vulnerability.fixed)

    def test_mark_vulnerabilities_fixed_no_cve_id(self):
        url = reverse('mark_vulnerabilities_fixed')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Body is empty or missing cve_id'})

    def test_mark_vulnerabilities_fixed_non_existent(self):
        url = reverse('mark_vulnerabilities_fixed')
        data = {'cve_id': 'CVE-9999-9999'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'No vulnerability found for the provided CVE ID'})

    def test_get_unfixed_vulnerabilities(self):
        self.vulnerability.fixed = False
        self.vulnerability.save()
        url = reverse('get_unfixed_vulnerabilities')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_vulnerabilities_summary_by_severity(self):
        url = reverse('get_vulnerabilities_summary_by_severity')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['base_severity'], 'HIGH')
        self.assertEqual(response.data[0]['count'], 1)