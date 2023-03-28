from itertools import chain

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as rest_reverse
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from .test_set import TestBugreport
from ..serializers import ListProjectSerializer, DetailsProjectSerializer, WriteProjectSerializer
from ..models import Project

UserModel = get_user_model()

class TestProject(TestBugreport):

    @TestBugreport.use_test_set
    def test_create_success(self):
        create_link = reverse_lazy('bugreport:project-list')
        user_index = 1
        user_data = {
            **self.get_user_tokens(user_index),
            'user': self.test_set['users'][user_index]
        }
        initial_porject_number = len(Project.objects.all())
        response = self.client.post(
            path=create_link,
            data = self.test_set_data['project'],
            HTTP_AUTHORIZATION=f'Bearer {user_data["access"]}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(Project.objects.all()),
            initial_porject_number + 1
        )
        self.assertEqual(
            response.json(),
            DetailsProjectSerializer(self.test_set['users'][user_index].projects.all()[0]).data
        )

    @TestBugreport.use_test_set
    def test_create_error(self):
        create_link = reverse_lazy('bugreport:project-list')
        # Create without auth token return 403
        response = self.client.post(
            path=create_link,
            data = self.test_set_data['project']
        )
        self.assertEqual(response.status_code, 403)
        # Create without data or missing data return 400
        user_data = self.get_user_tokens(1)
        response = self.client.post(
            path=create_link,
            data = {},
            HTTP_AUTHORIZATION=f'Bearer {user_data["access"]}'
        )
        self.assertEqual(response.status_code, 400)
    
    @TestBugreport.use_test_set
    def test_list_success(self):
        list_link = reverse_lazy('bugreport:project-list')
        for user_index in range(len(self.test_set_data['users'])):
            user_token = self.get_user_tokens(user_index)['access']
            response = self.client.get(
                path=list_link,
                HTTP_AUTHORIZATION=f'Bearer {user_token}'
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json(),
                ListProjectSerializer(
                    chain(
                        self.test_set['users'][user_index].projects.all(),
                        self.test_set['users'][user_index].contrib_projects.all()
                    ),
                    many=True
                ).data
            )
    
    def test_list_error(self):
        # list without auth token return 403
        list_link = reverse_lazy('bugreport:project-list')
        response = self.client.get(
            path=list_link
        )
        self.assertEqual(response.status_code, 403)
    
    @TestBugreport.use_test_set
    def test_retrieve_success(self):
        # retrieve a project return one project
        retrieve_link = rest_reverse('bugreport:project-detail', kwargs={'pk': self.test_set['project'].id})
        user_index = 0
        user_token = self.get_user_tokens(user_index)['access']
        response = self.client.get(
            path=retrieve_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            DetailsProjectSerializer(self.test_set['project']).data
        )
   
    @TestBugreport.use_test_set
    def test_retrieve_rerror(self):
        # retrieve request without token return 403
        retrieve_link = rest_reverse('bugreport:project-detail', kwargs={'pk': self.test_set['project'].id})
        response = self.client.get(
            path=retrieve_link
        )
        self.assertEqual(response.status_code, 403)
        # retrieve request withbad id return 404
        retrieve_link = rest_reverse('bugreport:project-detail', kwargs={'pk': self.test_set['project'].id+10})
        user_index = 0
        user_token = self.get_user_tokens(user_index)['access']
        response = self.client.get(
            path=retrieve_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 404)

    @TestBugreport.use_test_set
    def test_update_success(self):
        retrieve_link = rest_reverse('bugreport:project-detail', kwargs={'pk': self.test_set['project'].id})
        user_index = 0
        user_token = self.get_user_tokens(user_index)['access']
        response = self.client.put(
            path=retrieve_link,
            data={
                'title': 'title',
                **{
                    key: value
                    for key, value in WriteProjectSerializer(self.test_set['project']).data.items()
                    if key != 'title'
                }
            },
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Project.objects.get(id=self.test_set['project'].id).title,
            'title'
        )
    
    @TestBugreport.use_test_set
    def test_update_error(self):
        retrieve_link = rest_reverse('bugreport:project-detail', kwargs={'pk': self.test_set['project'].id})

        # Update a project without owning it return 403
        user_index = 1
        user_token = self.get_user_tokens(user_index)['access']
        response = self.client.put(
            path=retrieve_link,
            data={
                'title': 'title',
                **{
                    key: value
                    for key, value in WriteProjectSerializer(self.test_set['project']).data.items()
                    if key != 'title'
                }
            },
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 403)

        # Update a project without token return 403
        response = self.client.put(
            path=retrieve_link,
            data={
                'title': 'title',
                **{
                    key: value
                    for key, value in WriteProjectSerializer(self.test_set['project']).data.items()
                    if key != 'title'
                }
            }
        )
        self.assertEqual(response.status_code, 403)

        # Update a project without data return 400
        user_index = 0
        user_token = self.get_user_tokens(user_index)['access']
        response = self.client.put(
            path=retrieve_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 400)

        # Update a project with wrong id return 404
        retrieve_link = rest_reverse('bugreport:project-detail', kwargs={'pk': self.test_set['project'].id+10})
        user_index = 0
        user_token = self.get_user_tokens(user_index)['access']
        response = self.client.put(
            path=retrieve_link,
            data={
                'title': 'title',
                **{
                    key: value
                    for key, value in WriteProjectSerializer(self.test_set['project']).data.items()
                    if key != 'title'
                }
            },
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 404)

    @TestBugreport.use_test_set
    def test_delete_success(self):
        retrieve_link = rest_reverse('bugreport:project-detail', kwargs={'pk': self.test_set['project'].id})
        user_index = 0
        user_token = self.get_user_tokens(user_index)['access']
        response = self.client.delete(
            path=retrieve_link,
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        self.assertEqual(response.status_code, 200)
        is_delete = False
        try:
            Project.objects.get(id=self.test_set['project'].id)
        except Project.DoesNotExist:
            is_delete = True
        self.assertTrue(is_delete)
    
    @TestBugreport.use_test_set
    def test_delete_error(self):
        retrieve_link = rest_reverse('bugreport:project-detail', kwargs={'pk': self.test_set['project'].id})
        # Delete a project without owning it return 403
        for user_index in range(len(self.test_set['users'])):
            if self.test_set['users'][user_index].id != self.test_set['project'].author_user_id.id:
                user_token = self.get_user_tokens(user_index)['access']
                response = self.client.delete(
                    path=retrieve_link,
                    HTTP_AUTHORIZATION=f'Bearer {user_token}'
                )
                self.assertEqual(response.status_code, 403)
                is_delete = True
                try:
                    Project.objects.get(id=self.test_set['project'].id)
                except Project.DoesNotExist:
                    is_delete = False
                self.assertTrue(is_delete)
        # Delete a project without token return 403
        response = self.client.delete(
            path=retrieve_link,
        )
        self.assertEqual(response.status_code, 403)
        is_delete = True
        try:
            Project.objects.get(id=self.test_set['project'].id)
        except Project.DoesNotExist:
            is_delete = False
        self.assertTrue(is_delete)
        