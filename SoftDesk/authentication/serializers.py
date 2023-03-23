from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class BaseUserModelSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
        ]

class UserModelSerializer(BaseUserModelSerializer):
    pass

class SimpleUserSerializer(BaseUserModelSerializer):
    class Meta(BaseUserModelSerializer.Meta):
        fields = [
            'email',
            'id',
            'first_name',
            'last_name'
        ]
    