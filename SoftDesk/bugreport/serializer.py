from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

from .models import Project, Contributor


class SimpleUserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'id'
        ]


class ContributorSerializer(ModelSerializer):
    user = SimpleUserSerializer()
    class Meta:
        model = Contributor
        fields = [
            'user',
            'permission',
            'role'
        ]


class ProjectSerializer(ModelSerializer):
    author_user_id = SimpleUserSerializer()
    contributors_connection = ContributorSerializer(many=True)
    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'project_type',
            'author_user_id',
            'contributors_connection'
        ]
