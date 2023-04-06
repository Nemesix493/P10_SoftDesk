from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from ..serializers import WriteCommentSerializer, IssueListCommentSerializer, DetailsCommentSerializer
from ..models import Comment, Project, Issue
from ..exceptions import BadRequest, AccesDenied
from ..permissions import CustomCommentPermission, CustomIssuePermission


UserModel = get_user_model()

class CommentViewset(ModelViewSet):

    list_serializer_class = IssueListCommentSerializer
    write_serializer_class = WriteCommentSerializer
    details_serializer_class = DetailsCommentSerializer

    permission_classes = [CustomCommentPermission]

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
    
    def get_issue(self, pk):
        if pk is None:
            raise BadRequest()
        try:
            issue = Issue.objects.get(id=int(pk))
        except Issue.DoesNotExist:
            raise NotFound('Issue not found !')
        if not self.request.user in [issue.assignee_user_id, issue.author_user_id]:
            raise AccesDenied()
        return issue

    def get_object(self, pk):
        if pk is None:
            raise BadRequest()
        try:
            comment = Comment.objects.get(id=int(pk))
        except Comment.DoesNotExist:
            raise NotFound('Comment not found !')
        if self.check_object_permissions(self.request, comment):
            raise AccesDenied()
        return comment

    def create(self, request, project_pk=None, issue_pk=None):
        project = self.get_project(project_pk)
        issue = self.get_issue(issue_pk)
        serializer = self.write_serializer_class(data=request.data)
        if issue.project != project:
            raise BadRequest()
        if not serializer.is_valid():
            raise BadRequest()
        comment = serializer.unsave_create()
        comment.author_user_id = request.user
        comment.issue_id = issue
        comment.save()
        return Response(self.details_serializer_class(comment).data)
    
    def list(self, request, project_pk=None, issue_pk=None):
        project = self.get_project(project_pk)
        issue = self.get_issue(issue_pk)
        if issue.project != project:
            raise BadRequest()
        serializer =  self.list_serializer_class(issue.comments, many=True)
        return Response(serializer.data)
    
    def update(self, request, project_pk=None, issue_pk=None, pk=None):
        project = self.get_project(project_pk)
        issue = self.get_issue(issue_pk)
        comment = self.get_object(pk)
        serializer = self.write_serializer_class(
            comment,
            data=request.data
        )
        if issue.project != project or comment not in issue.comments.all():
            raise BadRequest()
        if not serializer.is_valid():
            raise BadRequest()
        comment = serializer.save()
        return Response(self.details_serializer_class(comment).data)

    def destroy(self, request, project_pk=None, issue_pk=None, pk=None):
        project = self.get_project(project_pk)
        issue = self.get_issue(issue_pk)
        comment = self.get_object(pk)
        if issue.project != project or comment not in issue.comments.all():
            raise BadRequest()
        serializer = self.details_serializer_class(comment)
        data = {
            'details': 'You corectly remove the following Issue !',
            'project': serializer.data,
        }
        comment.delete()
        return Response(data)
    
    def retrieve(self, request, project_pk=None, issue_pk=None, pk=None):
        project = self.get_project(project_pk)
        issue = self.get_issue(issue_pk)
        comment = self.get_object(pk)
        if issue.project != project or comment not in issue.comments.all():
            raise BadRequest()
        serializer = self.details_serializer_class(comment)
        return Response(serializer.data)

