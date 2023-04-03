from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model

from ..exceptions import AccesDenied, BadRequest
from ..models import Project, Issue
from ..permissions import CustomProjectPermission, CustomIssuePermission
from ..serializers import ProjectListIssueSerializer, WriteIssueSerializer, DetailsIssueSerializer


UserModel = get_user_model()


class IssuesViewset(ModelViewSet):
    list_serializer_class = ProjectListIssueSerializer
    write_serializer_class = WriteIssueSerializer
    details_serializer_class = DetailsIssueSerializer
    

    permission_classes = [CustomIssuePermission]

    def get_project(self, pk):
        if pk is None:
            raise BadRequest()
        try:
            project = Project.objects.get(id=int(pk))
        except Project.DoesNotExist:
            raise NotFound('Project not found !')
        if self.request.user not in [*project.contributors.all(), project.author_user_id]:
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
    
    def get_user(self, pk):
        if pk is None:
            raise BadRequest()
        try:
            user = UserModel.objects.get(id=pk)
        except UserModel.DoesNotExist:
            raise NotFound('User not found !')
        return user

    @staticmethod
    def check_assignee_user_id(assignee_user, project):
        return assignee_user in [*project.contributors.all(), project.author_user_id]

    def list(self, request, project_pk=None):
        project = self.get_project(project_pk)
        serializer = self.list_serializer_class(project.issues.all(), many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        raise BadRequest()
    
    def create(self, request, project_pk=None):
        project = self.get_project(project_pk)
        assignee_user = self.get_user(pk=request.data.get('assignee_user_id', None))
        if not self.check_assignee_user_id(assignee_user, project):
            raise BadRequest()
        serializer = self.write_serializer_class(data=request.data)
        if not serializer.is_valid():
            raise BadRequest()
        issue = serializer.unsave_create()
        issue.project = project
        issue.author_user_id = request.user
        issue.assignee_user_id = assignee_user
        issue.save()
        serializer = self.details_serializer_class(issue)
        return Response(serializer.data)
    
    def update(self, request, project_pk=None, pk=None):
        issue = self.get_object(pk)
        if project_pk != issue.project.id:
            raise BadRequest()
        project = self.get_project(project_pk)
        assignee_user = self.get_user(pk=request.data.get('assignee_user_id', None))
        if not self.check_assignee_user_id(assignee_user, project):
            raise BadRequest()
        serializer = self.write_serializer_class(issue, data=request.data)
        if not serializer.is_valid():
            raise BadRequest()
        issue = serializer.save()
        issue.assignee_user_id = assignee_user
        issue.save()
        serializer = self.details_serializer_class(issue)
        return Response(serializer.data)
    
    def destroy(self, request, project_pk=None, pk=None):
        issue = self.get_object(pk)
        if project_pk != issue.project.id:
            raise BadRequest()
        serializer = self.details_serializer_class(issue)
        data = {
            'details': 'You corectly remove the following Issue !',
            'project': serializer.data,
        }
        issue.delete()
        return Response(data)