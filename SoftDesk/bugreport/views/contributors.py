from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from ..serializers import DetailsProjectSerializer, DetailsContributorSerializer, ListContributorSerializer, WriteContributorSerializer
from ..models import Project, Contributor
from ..permissions import CustomProjectPermission, CustomContributorPermission
from ..exceptions import BadRequest, AccesDenied


UserModel = get_user_model()



class ContributorViewset(ModelViewSet):
    list_serializer_class = ListContributorSerializer
    write_serializer_class = WriteContributorSerializer
    project_details_serializer_class = DetailsProjectSerializer

    permission_classes = [CustomContributorPermission]

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

    def list(self, request, project_pk=None):
        project = self.get_project(project_pk)
        serializer = ListContributorSerializer(project.contributors_connection.all(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        raise BadRequest()
    
    def create(self, request, project_pk=None):
        project = self.get_project(project_pk)
        # Check if new contributor is not already a contribor
        try:
            if request.data.get('user', None) is None:
                raise BadRequest()
            user = UserModel.objects.get(id=request.data.get('user', None))
            if user in [*project.contributors.all(), project.author_user_id]:
                raise BadRequest(detail='User already contributor !')
        except UserModel.DoesNotExist:
            raise NotFound(detail='New contributor not found !')
        serializer = self.write_serializer_class(data=request.data)
        if not serializer.is_valid():
            raise BadRequest()
        contributor = serializer.unsave_create()
        contributor.project = project
        contributor.save()
        serializer = self.project_details_serializer_class(project)
        return Response(serializer.data)

    def destroy(self, request, pk=None, project_pk=None):
        project = self.get_project(project_pk)
        try:
            user = UserModel.objects.get(id=pk)
        except UserModel.DoesNotExist:
            raise NotFound('User not found !')
        try:
            contributor = Contributor.objects.get(
                project=project,
                user=user
            )
            contributor.delete()
        except Contributor.DoesNotExist:
            raise NotFound('Contributor not found !')
        serializer = DetailsContributorSerializer(contributor)
        data = {
            'details': 'You corectly remove the following Contributor !',
            'contributor': serializer.data,
        }
        return Response(data)
