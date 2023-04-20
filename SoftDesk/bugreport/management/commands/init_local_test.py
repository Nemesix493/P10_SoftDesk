from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from bugreport.models import Project

UserModel = get_user_model()

ADMIN_ID = 'kevin'
ADMIN_PASSWORD = 'Kevin-root'

PROJECTS = [
    {
        'title':'SoftDesk',
        'description': 
            "Lorem ipsum dolor sit amet, consectetur adipisicing elit.\n"
            "Voluptates cupiditate ducimus deserunt ea repellat! Nobis excepturi odio dolor atque totam vero impedit facilis officia, consectetur velit ipsum nisi in id?",
        'project_type': 'django rest framwork',
    }
]

USERS = [
    {
        'first_name': 'Daniel',
        'password': 'motdepasse',
        'last_name': 'last-name'
    },
    {
        'first_name': 'Serge',
        'password': 'motdepasse',
        'last_name': 'last-name'
    },
    {
        'first_name': 'Claude',
        'password': 'motdepasse',
        'last_name': 'last-name'
    },
]

class Command(BaseCommand):

    help = 'Initialize project for local tests'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))
        UserModel.objects.all().delete()
        adm = UserModel.objects.create(email=ADMIN_ID + '@oc.drf', is_superuser=True)
        adm.set_password(ADMIN_PASSWORD)
        adm.save()
        for user in USERS:
            current_user = UserModel.objects.create(email=user['first_name'] + '@SoftDesk.com')
            current_user.first_name = user['first_name']
            current_user.last_name = user['last_name']
            current_user.set_password(user['password'])
            current_user.save()
            for serialized_project in PROJECTS:
                project = Project.objects.create(author_user_id=current_user, **serialized_project)
                project.title = project.title + ' ' + user['first_name']
                project.save()
        self.stdout.write(self.style.SUCCESS('All Done !'))
