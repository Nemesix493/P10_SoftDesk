from rest_framework.serializers import ModelSerializer


class WriteSerializer(ModelSerializer):
    def unsave_create(self):
        return self.Meta.model(**self.validated_data)