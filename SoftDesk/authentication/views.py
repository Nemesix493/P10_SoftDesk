from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .serializers import UserModelSerializer

UserModel = get_user_model()

@api_view(['POST'])
def create_user(request):
    user_serializer = UserModelSerializer(data=request.data)
    if user_serializer.is_valid():
        user = UserModel(
            **user_serializer.data
        )
        password = request.data.get('password', '')
        try:
            validate_password(password)
        except ValidationError:
            return Response(
                {
                    'details': 'password not valid'
                },
                status=400
            )
        user.set_password(password)
        user.save()
        return Response(UserModelSerializer(user).data)
    return Response(
                {
                    'details': 'data not valid',
                    'error': user_serializer.error_messages
                },
                status=400
            )