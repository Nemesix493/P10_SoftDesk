from rest_framework.serializers import ModelSerializer

from ..models import Issue
from .base import WriteSerializer
from authentication.serializers import SimpleUserSerializer

class BaseIssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'description',
            'tag',
            'priority',
            'status',
            'created_time',  
        ]


class WriteIssueSerializer(BaseIssueSerializer, WriteSerializer):
    pass


class ProjectListIssueSerializer(BaseIssueSerializer):
    class Meta(BaseIssueSerializer.Meta):
        fields = [
            *BaseIssueSerializer.Meta.fields,
            'author_user_id',
            'assignee_user_id'
        ]


class DetailsIssueSerializer(BaseIssueSerializer):
    author_user_id = SimpleUserSerializer()
    assignee_user_id = SimpleUserSerializer()
    class Meta(BaseIssueSerializer.Meta):
        fields = [
            *BaseIssueSerializer.Meta.fields,
            'project',
            'author_user_id',
            'assignee_user_id'
        ]
