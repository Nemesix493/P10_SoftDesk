from rest_framework.test import APITestCase
from django.urls import reverse_lazy

from .test_set import TestBugreport
from ..serializers import IssueListCommentSerializer, DetailsCommentSerializer
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
    def test_update_success(self):
        detail_link = reverse_lazy(
            'bugreport:comments-detail',
            kwargs={
                'project_pk': self.test_set['project'].id,
                'issue_pk': self.test_set['issue'].id,
                'pk': self.test_set['comment'].id
            }
        )
        user_token = self.get_user_tokens(3)['access']
        response = self.client.put(
            path=detail_link,
            data={
                'description': 'new-description'
            },
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Comment.objects.get(id=self.test_set['comment'].id).description,
            'new-description'
        )

    @TestBugreport.use_test_set
    def test_update_error(self):
        detail_link = reverse_lazy(
            'bugreport:comments-detail',
            kwargs={
                'project_pk': self.test_set['project'].id,
                'issue_pk': self.test_set['issue'].id,
                'pk': self.test_set['comment'].id
            }
        )
        # update without auth token return 403
        response = self.client.put(
            path=detail_link,
            data={
                'description': 'description'
            },
        )
        self.assertEqual(response.status_code, 403)
        # update without contribute in the project return 403
        user_token = self.get_user_tokens(2)['access']
        response = self.client.put(
            path=detail_link,
            data={
                'description': 'description'
            },
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 403)
        # update without data return 400
        user_token = self.get_user_tokens(3)['access']
        response = self.client.put(
            path=detail_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 400)
        # update without owning the comment return 403
        user_token = self.get_user_tokens(1)['access']
        response = self.client.put(
            path=detail_link,
            data={
                'description': 'description'
            },
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 403)

    @TestBugreport.use_test_set
    def test_destroy_success(self):
        detail_link = reverse_lazy(
            'bugreport:comments-detail',
            kwargs={
                'project_pk': self.test_set['project'].id,
                'issue_pk': self.test_set['issue'].id,
                'pk': self.test_set['comment'].id
            }
        )
        user_token = self.get_user_tokens(3)['access']
        response = self.client.delete(
            path=detail_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 200)
        try:
            Comment.objects.get(id=self.test_set['comment'].id)
            self.assertTrue(False, msg=f'The comment is not destroyed because otherwise the orm would have to raise {Comment.DoesNotExist}')
        except Comment.DoesNotExist:
            self.assertTrue(True)

    @TestBugreport.use_test_set
    def test_destroy_error(self):
        detail_link = reverse_lazy(
            'bugreport:comments-detail',
            kwargs={
                'project_pk': self.test_set['project'].id,
                'issue_pk': self.test_set['issue'].id,
                'pk': self.test_set['comment'].id
            }
        )
        # destroy without auth token return 403
        response = self.client.delete(
            path=detail_link
        )
        self.assertEqual(response.status_code, 403)
        # destroy without owning the comment return 403
        user_token = self.get_user_tokens(1)['access']
        response = self.client.delete(
            path=detail_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 403)

    @TestBugreport.use_test_set
    def test_retrieve_success(self):
        detail_link = reverse_lazy(
            'bugreport:comments-detail',
            kwargs={
                'project_pk': self.test_set['project'].id,
                'issue_pk': self.test_set['issue'].id,
                'pk': self.test_set['comment'].id
            }
        )
        user_token = self.get_user_tokens(3)['access']
        response = self.client.get(
            path=detail_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            DetailsCommentSerializer(self.test_set['comment']).data
        )

    @TestBugreport.use_test_set
    def test_retrieve_error(self):
        detail_link = reverse_lazy(
            'bugreport:comments-detail',
            kwargs={
                'project_pk': self.test_set['project'].id,
                'issue_pk': self.test_set['issue'].id,
                'pk': self.test_set['comment'].id
            }
        )
        # destroy without auth token return 403
        response = self.client.get(
            path=detail_link
        )
        self.assertEqual(response.status_code, 403)
        # retriev without contribute the project return 403
        user_token = self.get_user_tokens(2)['access']
        response = self.client.get(
            path=detail_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 403)
        