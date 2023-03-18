from django.urls import reverse
from rest_framework.permissions import BasePermission

from .exceptions import LoginRequired, AccesDenied


class CustomProjectPermission(BasePermission):
    message = 'Try again'
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise LoginRequired(reverse('token_obtain_pair'))
        return True
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            raise LoginRequired(reverse('token_obtain_pair'))
        #The user try to modify anything he don't own
        if request.method != 'GET' and request.user != obj.author_user_id:
            raise AccesDenied()
        return True
