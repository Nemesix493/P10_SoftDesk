from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from ..models import Project, Contributor, Issue

UserModel = get_user_model()

class TestBugreport(APITestCase):
    test_set_data = {
        'users':[
            {
                'email': f'user{i+1}@oc.drf',
                'first_name': f'user{i+1}',
                'last_name': 'test',
                'password': 'motdepasse'
            } for i in range(4)
        ],
        'project':{
            'title': 'ProjectTestTitle',
            'description': 'ProjectTestDescription',
            'project_type': 'ProjectTestType',
        },
        'contributor':{
            'permission': 'WRITE',
            'role': 'DEV-BACk'
        },
        'issue':{
            'title': 'IssueTestTitle',
            'description': 'IssueTestDescription',
            'tag': 'IssueTestTag',
            'priority': 'IssueTestPriority',
            'status': 'IssueTestStatus',
        }
    }

    def create_user(self, **kwargs) -> UserModel:
        user = get_user_model().objects.create(
            **{
                key: val
                for key, val in kwargs.items()
                if key != 'password'
            }
        )
        user.set_password(kwargs['password'])
        user.save()
        return user
    
    def create_project(self, project_data, user: UserModel) -> Project:
        project = Project.objects.create(
            **project_data,
            author_user_id = user
        )
        project.save()
        return project

    def get_test_set(self):
        self.test_set = {
            'users': [
                self.create_user(**user_data)
                for user_data in self.test_set_data['users']
            ]
        }
        self.test_set['project'] = self.create_project(self.test_set_data['project'], self.test_set['users'][0])
        for contrib_index in [1, 3]:
            contributor = Contributor.objects.create(
                project=self.test_set['project'],
                user=self.test_set['users'][contrib_index],
                **self.test_set_data['contributor']
            )
        self.test_set['issue'] = Issue.objects.create(
            project = self.test_set['project'],
            author_user_id=self.test_set['users'][1],
            assignee_user_id=self.test_set['users'][3],
            **self.test_set_data['issue']
        )

            
    def get_user_tokens(self, user_index: int):    
        login_link = reverse_lazy('token_obtain_pair')
        response = self.client.post(
            path=login_link,
            data=self.test_set_data['users'][user_index]
        )
        return response.json()
    
    @staticmethod
    def use_test_set(func):
        def decorate_function(self, *args, **kwargs):
            self.get_test_set()
            return func(self, *args, **kwargs)
        return decorate_function