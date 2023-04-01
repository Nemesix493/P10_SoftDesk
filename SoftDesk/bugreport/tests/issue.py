from rest_framework.test import APITestCase
from django.urls import reverse_lazy

from .test_set import TestBugreport
from ..serializers import ProjectListIssueSerializer

class TestIssue(TestBugreport):

    @TestBugreport.use_test_set
    def test_list_success(self):
        list_link = reverse_lazy('bugreport:issues-list', kwargs={'project_pk': self.test_set['project'].id})
        user_token = self.get_user_tokens(0)['access']
        response = self.client.get(
            path=list_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            ProjectListIssueSerializer(self.test_set['project'].issues.all(), many=True).data
        )
        
    @TestBugreport.use_test_set
    def test_list_error(self):
        # list without auth token return 403
        list_link = reverse_lazy('bugreport:issues-list', kwargs={'project_pk': self.test_set['project'].id})
        response = self.client.get(
            path=list_link
        )
        self.assertEqual(response.status_code, 403)
        # list issues of a project without owning it return 403
        user_token = self.get_user_tokens(2)['access']
        response = self.client.get(
            path=list_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 403)
    
    @TestBugreport.use_test_set
    def test_create_success(self):
        list_link = reverse_lazy('bugreport:issues-list', kwargs={'project_pk': self.test_set['project'].id})
        user_token = self.get_user_tokens(0)['access']
        user_id = self.test_set['users'][0].id
        response = self.client.post(
            path=list_link,
            data={
                'assignee_user_id': user_id,
                'title': 'title',
                'description': 'description',
                'tag': 'tag',
                'priority': 'priority',
                'status': 'status',
            },
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 200)
    
    @TestBugreport.use_test_set
    def test_create_error(self):
        list_link = reverse_lazy('bugreport:issues-list', kwargs={'project_pk': self.test_set['project'].id})
        # create without auth token return 403
        user_id = self.test_set['users'][0].id
        response = self.client.post(
            path=list_link,
            data={
                'assignee_user_id': user_id,
                'title': 'title',
                'description': 'description',
                'tag': 'tag',
                'priority': 'priority',
                'status': 'status',
            }
        )
        self.assertEqual(response.status_code, 403)
        # create without data token return 400
        user_token = self.get_user_tokens(0)['access']
        user_id = self.test_set['users'][0].id
        response = self.client.post(
            path=list_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 400)

