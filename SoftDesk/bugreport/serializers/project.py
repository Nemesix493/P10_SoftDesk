from rest_framework.serializers import ModelSerializer

from .base import WriteSerializer
from ..models import Project
from authentication.serializers import SimpleUserSerializer


class BaseProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'project_type'
        ]


class WriteProjectSerializer(BaseProjectSerializer, WriteSerializer):
    pass


class DetailsProjectSerializer(BaseProjectSerializer):
    author_user = SimpleUserSerializer(source='author_user_id')
    class Meta(BaseProjectSerializer.Meta):
        fields = [
            *BaseProjectSerializer.Meta.fields,
            'id',
            'author_user',
            'contributors'
        ]


class ListProjectSerializer(BaseProjectSerializer):
    class Meta(BaseProjectSerializer.Meta):
        fields = [
            *BaseProjectSerializer.Meta.fields,
            'id',
            'author_user_id'
        ]