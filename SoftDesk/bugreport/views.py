from itertools import chain

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework.exceptions import NotFound, APIException
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .serializer import ProjectSerializer
from .models import Project, Contributor
from .permissions import CustomProjectPermission
from .exceptions import BadRequest, AccesDenied


UserModel = get_user_model()


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [CustomProjectPermission]
    def list(self, request):
        if request.user.is_superuser:
            queryset = Project.objects.all()
            serializer = ProjectSerializer(queryset, many=True)
            return Response(serializer.data)
        queryset = chain(
            request.user.contrib_projects.all(),
            request.user.projects.all()
        )
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        project_data = request.data
        new_project = Project.objects.create(
            title=project_data['title'],
            description=project_data['description'],
            project_type=project_data['project_type'],
            author_user_id=request.user,
        )
        new_project.save()
        serializer = ProjectSerializer(new_project)
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'], url_path='user')
    def add_contributor(self, request, pk):
        contributor_data = request.data
        # Check if project exist
        try:
            project = Project.objects.get(id=pk)
        except Project.DoesNotExist:
            raise NotFound()
        # Check has_object_permission
        if False in [
            permission_classe().has_object_permission(
                request=request,
                view=self,
                obj=project
            ) for permission_classe in self.permission_classes]:
            raise AccesDenied()
        # Check if new contributor exist
        try:
            user = UserModel.objects.get(id=int(contributor_data['user_id']))
        except UserModel.DoesNotExist:
            raise NotFound(detail='New contributor not found !')
        # Check if new contributor is not already a contribor
        if user in project.contributors.all():
            raise BadRequest(detail='User already contributor !')
        #Check data validity
        new_contributor = Contributor(
            project=project,
            role=contributor_data['role'],
            permission=contributor_data['permission'],
            user=user
        )
        try:
            new_contributor.clean_fields()
        except ValidationError as e:
            raise BadRequest(detail=str(e))
        new_contributor.save()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    @action(detail=True, methods=['POST', 'GET'], url_path='user/(?P<contrib>\w+)')
    def modify_contributor(self, request, pk, contrib):
        print(f'pk={pk}, contrib={contrib}')
        return Response(['test'])
