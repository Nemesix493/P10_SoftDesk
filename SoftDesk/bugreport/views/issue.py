from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model

from ..exceptions import AccesDenied, BadRequest
from ..models import Project, Issue
from ..permissions import CustomProjectPermission, CustomIssuePermission
from ..serializers import ProjectListIssueSerializer


UserModel = get_user_model()


class IssuesViewset(ModelViewSet):
    list_serializer_class = ProjectListIssueSerializer

    permission_classes = [CustomIssuePermission]

    def get_project(self, pk):
        if pk is None:
            raise BadRequest()
        try:
            project = Project.objects.get(id=int(pk))
        except Project.DoesNotExist:
            raise NotFound('Project not found !')
        if not CustomProjectPermission().has_object_permission(self.request, self, project):
            raise AccesDenied()
        return project
    
    def get_object(self, pk):
        if pk is None:
            raise BadRequest()
        try:
            issue = Issue.objects.get(id=int(pk))
        except Issue.DoesNotExist:
            raise NotFound('Project not found !')
        if self.check_object_permissions(self.request, issue):
            raise AccesDenied()
        return issue
    
    def list(self, request, project_pk=None):
        project = self.get_project(project_pk)
        serializer = self.list_serializer_class(project.issues.all(), many=True)
        return Response(serializer.data)