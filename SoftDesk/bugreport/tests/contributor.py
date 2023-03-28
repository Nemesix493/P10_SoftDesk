from rest_framework.test import APITestCase
from django.urls import reverse_lazy

from .test_set import TestBugreport
from ..serializers import ListContributorSerializer

class TestContributor(TestBugreport):

    @TestBugreport.use_test_set
    def test_list_success(self):
        list_link = reverse_lazy('bugreport:users-list', kwargs={'project_pk': self.test_set['project'].id})
        user_token = self.get_user_tokens(0)['access']
        response = self.client.get(
            path=list_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            ListContributorSerializer(self.test_set['project'].contributors_connection.all(), many=True).data
        )
    
    @TestBugreport.use_test_set
    def test_list_error(self):
        # list without auth token return 403
        list_link = reverse_lazy('bugreport:users-list', kwargs={'project_pk': self.test_set['project'].id})
        response = self.client.get(
            path=list_link
        )
        self.assertEqual(response.status_code, 403)
        # list contributor of a project without owning it return 403
        user_token = self.get_user_tokens(2)['access']
        response = self.client.get(
            path=list_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 403)