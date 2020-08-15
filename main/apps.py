import sys

from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        if 'runserver' not in sys.argv:  # TODO возможно не запуститься через wsgi
            return True
        from main import tasks
        #tasks.session_creator()
