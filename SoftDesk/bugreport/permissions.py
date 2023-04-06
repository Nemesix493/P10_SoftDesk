from itertools import chain

from django.urls import reverse
from rest_framework.permissions import BasePermission

from .exceptions import LoginRequired, AccesDenied
from .models import Project, Issue, Comment

class CustomBasePermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise LoginRequired(reverse('token_obtain_pair'))
        return True

class CustomProjectPermission(CustomBasePermission):
    def has_object_permission(self, request, view, obj: Project):
        if not request.user.is_authenticated:
            raise LoginRequired(reverse('token_obtain_pair'))
        if view.action in ['retrieve', 'list'] and request.user not in [*obj.contributors.all(), obj.author_user_id]:
            raise AccesDenied()
        #The user try to modify anything he don't own
        if request.method != 'GET' and request.user != obj.author_user_id:
            raise AccesDenied()
        return True

class CustomContributorPermission(CustomBasePermission):
    pass

class CustomIssuePermission(CustomBasePermission):
    def has_object_permission(self, request, view, obj: Issue):
        if not request.user.is_authenticated:
            raise LoginRequired(reverse('token_obtain_pair'))
        #The user try to modify anything he don't own
        if request.method != 'GET' and request.user != obj.author_user_id:
            raise AccesDenied()
        return True

class CustomCommentPermission(CustomBasePermission):
    def has_object_permission(self, request, view, obj: Comment):
        if not request.user.is_authenticated:
            raise LoginRequired(reverse('token_obtain_pair'))
        #The user try to modify anything he don't own
        if request.method != 'GET' and request.user != obj.author_user_id:
            raise AccesDenied()
        return True
    
