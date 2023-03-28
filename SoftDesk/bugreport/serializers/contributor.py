from rest_framework.serializers import ModelSerializer

from ..models import Contributor
from .base import WriteSerializer
from authentication.serializers import SimpleUserSerializer


class BaseContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = [
            'user',
            'permission',
            'role'
        ]


class WriteContributorSerializer(BaseContributorSerializer, WriteSerializer):
    pass


class ListContributorSerializer(BaseContributorSerializer):
    user = SimpleUserSerializer()


class DetailsContributorSerializer(BaseContributorSerializer):
    user = SimpleUserSerializer()
    class Meta(BaseContributorSerializer.Meta):
        fields = [
            *BaseContributorSerializer.Meta.fields,
            'project'
        ]
