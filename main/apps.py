import os
import sys

from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        if 'runserver' not in sys.argv or os.environ.get("DISABLE_SESSIONCREATOR") is not None:  # TODO возможно не запуститься через wsgi
            return True

        if os.environ.get('RUN_MAIN') == 'true':
            from main import tasks
            tasks.session_creator()
