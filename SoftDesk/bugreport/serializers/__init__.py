from .project import WriteProjectSerializer, DetailsProjectSerializer, ListProjectSerializer
from .contributor import WriteContributorSerializer, DetailsContributorSerializer, ListContributorSerializer
from .issue import WriteIssueSerializer, DetailsIssueSerializer, ProjectListIssueSerializer, CommentDetailsIssueSerializer
from .comment import WriteCommentSerializer, IssueListCommentSerializer, DetailsCommentSerializer

DetailsProjectSerializer.contributors = ListContributorSerializer(many=True, source='contributors_connection')
DetailsContributorSerializer.project = ListProjectSerializer()
DetailsIssueSerializer.comments = IssueListCommentSerializer(many=True)
DetailsCommentSerializer.issue = CommentDetailsIssueSerializer(source='issue_id')
