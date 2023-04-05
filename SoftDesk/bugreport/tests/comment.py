from rest_framework.test import APITestCase
from django.urls import reverse_lazy

from .test_set import TestBugreport
from ..serializers import IssueListCommentSerializer
from ..models import Comment

class TestComment(TestBugreport):
    @TestBugreport.use_test_set
    def test_create_success(self):
        list_link = reverse_lazy('bugreport:comments-list', kwargs={'project_pk': self.test_set['project'].id, 'issue_pk': self.test_set['issue'].id})
        user_token = self.get_user_tokens(3)['access']
        response = self.client.post(
            path=list_link,
            data={
                'description': 'description'
            },
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 200)
    
    @TestBugreport.use_test_set
    def test_create_error(self):
        list_link = reverse_lazy('bugreport:comments-list', kwargs={'project_pk': self.test_set['project'].id, 'issue_pk': self.test_set['issue'].id})
        # create without auth token return 403
        response = self.client.post(
            path=list_link,
            data={
                'description': 'description'
            }
        )
        self.assertEqual(response.status_code, 403)
        # create without contribute in the project return 403
        user_token = self.get_user_tokens(2)['access']
        response = self.client.post(
            path=list_link,
            data={
                'description': 'description'
            },
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 403)
        # create without data return 400
        user_token = self.get_user_tokens(3)['access']
        response = self.client.post(
            path=list_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 400)

    @TestBugreport.use_test_set
    def test_list_success(self):
        list_link = reverse_lazy('bugreport:comments-list', kwargs={'project_pk': self.test_set['project'].id, 'issue_pk': self.test_set['issue'].id})
        user_token = self.get_user_tokens(3)['access']
        response = self.client.get(
            path=list_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            IssueListCommentSerializer([self.test_set['comment']], many=True).data
        )

    @TestBugreport.use_test_set
    def test_create_error(self):
        list_link = reverse_lazy('bugreport:comments-list', kwargs={'project_pk': self.test_set['project'].id, 'issue_pk': self.test_set['issue'].id})
        # create without auth token return 403
        response = self.client.get(
            path=list_link,
        )
        self.assertEqual(response.status_code, 403)
        # create without contribute in the project return 403
        user_token = self.get_user_tokens(2)['access']
        response = self.client.get(
            path=list_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 403)
    
    