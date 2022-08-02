import os
import pathlib
import sys

import django


def pytest_configure(config):
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'
    django.setup()
