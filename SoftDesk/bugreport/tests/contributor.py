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

    @TestBugreport.use_test_set
    def test_create_success(self):
        list_link = reverse_lazy('bugreport:users-list', kwargs={'project_pk': self.test_set['project'].id})
        user_token = self.get_user_tokens(0)['access']
        response = self.client.post(
            path=list_link,
            data={
                'user': self.test_set['users'][2].id,
                'permission': 'READ',
                'role': 'role'
            },
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 200)
    
    @TestBugreport.use_test_set
    def test_create_error(self):
        list_link = reverse_lazy('bugreport:users-list', kwargs={'project_pk': self.test_set['project'].id})
        # create without auth token return 403
        response = self.client.post(
            path=list_link,
            data={
                'user': self.test_set['users'][2].id,
                'permission': 'READ',
                'role': 'role'
            }
        )
        self.assertEqual(response.status_code, 403)
        # create without owning project return 403
        user_token = self.get_user_tokens(1)['access']
        response = self.client.post(
            path=list_link,
            data={
                'user': self.test_set['users'][2].id,
                'permission': 'READ',
                'role': 'role'
            },
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 403)
        # create without data project return 400
        user_token = self.get_user_tokens(0)['access']
        response = self.client.post(
            path=list_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 400)
        
    @TestBugreport.use_test_set
    def test_destroy_success(self):
        detail_link = reverse_lazy('bugreport:users-detail', kwargs={'project_pk': self.test_set['project'].id, 'pk': self.test_set['users'][1].id})
        user_token = self.get_user_tokens(0)['access']
        response = self.client.delete(
            path=detail_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 200)
    
    @TestBugreport.use_test_set
    def test_destroy_error(self):
        detail_link = reverse_lazy('bugreport:users-detail', kwargs={'project_pk': self.test_set['project'].id, 'pk': self.test_set['users'][1].id})
        # create without auth token return 403
        response = self.client.delete(
            path=detail_link,
        )
        self.assertEqual(response.status_code, 403)
        # create without owning project return 403
        user_token = self.get_user_tokens(1)['access']
        response = self.client.delete(
            path=detail_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 403)
