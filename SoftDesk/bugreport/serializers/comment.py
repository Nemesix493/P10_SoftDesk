from rest_framework.serializers import ModelSerializer

from ..models import Comment
from .base import WriteSerializer
from authentication.serializers import SimpleUserSerializer


class BaseCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'description'
        ]


class WriteCommentSerializer(BaseCommentSerializer, WriteSerializer):
    pass


class IssueListCommentSerializer(BaseCommentSerializer):
    class Meta(BaseCommentSerializer.Meta):
        fields = [
            'id',
            *BaseCommentSerializer.Meta.fields,
            'author_user_id',
            'created_time'
        ]


class DetailsCommentSerializer(BaseCommentSerializer):
    author_user = SimpleUserSerializer(source='author_user_id')
    class Meta(BaseCommentSerializer.Meta):
        fields = [
            'id',
            *BaseCommentSerializer.Meta.fields,
            'author_user',
            'issue_id',
            'created_time'
        ]