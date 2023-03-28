from itertools import chain

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model

from ..serializers import ListProjectSerializer, DetailsProjectSerializer, WriteProjectSerializer
from ..models import Project
from ..permissions import CustomProjectPermission
from ..exceptions import BadRequest, AccesDenied


UserModel = get_user_model()


class ProjectViewset(ModelViewSet):
    write_serializer_class = WriteProjectSerializer
    details_serializer_class = DetailsProjectSerializer
    list_serializer_class = ListProjectSerializer
    
    permission_classes = [CustomProjectPermission]

    def get_object(self, pk):
        if pk is None:
            raise BadRequest()
        try:
            project = Project.objects.get(id=int(pk))
        except Project.DoesNotExist:
            raise NotFound('Project not found !')
        if self.check_object_permissions(self.request, project):
            raise AccesDenied()
        return project
  
    def list(self, request):
        queryset = chain(
            request.user.contrib_projects.all(),
            request.user.projects.all()
        )
        serializer = self.list_serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.write_serializer_class(data=request.data)
        if not serializer.is_valid():
            raise BadRequest()
        project = serializer.unsave_create()
        project.author_user_id = request.user
        project.save()
        serializer = self.details_serializer_class(project)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        project = self.get_object(pk)
        serializer = self.details_serializer_class(project)
        return Response(serializer.data)

    def update(self, request, pk=None):
        project = self.get_object(pk)
        serializer = self.write_serializer_class(
            project,
            data=request.data
        )
        if not serializer.is_valid():
            raise BadRequest(serializer.errors)
        project = serializer.save()
        data = {
            'details': 'You corectly update the following Project !',
            'project': self.list_serializer_class(project).data,
        }
        return Response(data)
    
    def destroy(self, request, pk):
        project = self.get_object(pk)
        serializer = self.details_serializer_class(project)
        data = {
            'details': 'You corectly remove the following Project !',
            'project': serializer.data,
        }
        project.delete()
        return Response(data)
