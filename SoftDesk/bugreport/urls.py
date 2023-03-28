from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import ProjectViewset, ContributorViewset, IssuesViewset

project_router = SimpleRouter()
project_router.register('projects', ProjectViewset, basename='project')
subproject_router = SimpleRouter()
subproject_router.register('users', ContributorViewset, basename='users')
subproject_router.register('issues', IssuesViewset, basename='issues')

app_name = 'bugreport'
urlpatterns = [
    path('', include(project_router.urls)),
    path('projects/<int:project_pk>/', include(subproject_router.urls))
]
