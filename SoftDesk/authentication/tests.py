from rest_framework.test import APITestCase
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class TestAuthViews(APITestCase):
    def test_create_user_success(self):
        signup_link = reverse_lazy('signup')
        response = self.client.post(
            path=signup_link,
            data={
                'email': 'user.test@oc.drf',
                'first_name': 'user',
                'last_name': 'test',
                'password': '3i5mTqHSeMagJxg7qz4zJb7b'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(UserModel.objects.all()), 1)
    
    def test_create_user_error(self):
        signup_link = reverse_lazy('signup')
        # Create user with not valid password return 400
        response = self.client.post(
            path=signup_link,
            data={
                'email': 'user.test@oc.drf',
                'first_name': 'user',
                'last_name': 'test',
                'password': ''
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(UserModel.objects.all()), 0)
        # Create user with missing data return 400
        response = self.client.post(
            path=signup_link,
            data={
                'first_name': 'user',
                'last_name': 'test',
                'password': ''
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(UserModel.objects.all()), 0)

