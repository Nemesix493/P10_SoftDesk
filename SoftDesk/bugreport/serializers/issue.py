from rest_framework.serializers import ModelSerializer, Field

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
        ]


class WriteIssueSerializer(BaseIssueSerializer, WriteSerializer):
    pass


class ProjectListIssueSerializer(BaseIssueSerializer):
    class Meta(BaseIssueSerializer.Meta):
        fields = [
            *BaseIssueSerializer.Meta.fields,
            'created_time',  
            'author_user_id',
            'assignee_user_id'
        ]


class DetailsIssueSerializer(BaseIssueSerializer):
    author_user = SimpleUserSerializer(source='author_user_id')
    assignee_user = SimpleUserSerializer(source='assignee_user_id')
    class Meta(BaseIssueSerializer.Meta):
        fields = [
            *BaseIssueSerializer.Meta.fields,
            'created_time',  
            'project',
            'author_user',
            'assignee_user',
            'comments'
        ]

class CommentDetailsIssueSerializer(BaseIssueSerializer):
    project_id = Field(source='project')
    class Meta(BaseIssueSerializer.Meta):
        fields = [
            *BaseIssueSerializer.Meta.fields,
            'created_time',  
            'project_id',
            'author_user_id',
            'assignee_user_id'
        ]
