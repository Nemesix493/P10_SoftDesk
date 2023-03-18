from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator
# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)    
    project_type = models.CharField(max_length=50)
    author_user_id = models.ForeignKey(
        to=get_user_model(),
        related_name='projects',
        on_delete=models.CASCADE
    )
    contributors = models.ManyToManyField(
        to=get_user_model(),
        through='Contributor',
        related_name='contrib_projects',
        through_fields=('project', 'user'),
    )

class Contributor(models.Model):
    PERMISSION_CHOICES = [
        ('NONE', 'None'),
        ('READ', 'Read'),
        ('WRITE', 'Write')
    ]
    user = models.ForeignKey(
        to=get_user_model(),
        related_name='contrib_projects_connection',
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        to=Project,
        related_name='contributors_connection',
        on_delete=models.CASCADE
    )
    permission = models.CharField(
        max_length=5,
        choices=PERMISSION_CHOICES,
        default='NONE',
        validators=[MaxLengthValidator(5)]
    )
    role = models.CharField(max_length=50, validators=[MaxLengthValidator(50)])
    class Meta:
        unique_together = ('user', 'project',)

    
