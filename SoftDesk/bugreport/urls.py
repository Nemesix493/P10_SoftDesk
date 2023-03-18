from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import ProjectViewset

router = SimpleRouter()
router.register('project', ProjectViewset, basename='project')

app_name = 'bugreport'
urlpatterns = [
    path('', include(router.urls))
]
