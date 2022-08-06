import pathlib
import re

import setuptools

www_dir = pathlib.Path(__file__).parent
init = (www_dir.parent / 'django_rrweb' / '__init__.py').read_text()
match = re.search(r"^__version__ = '(.+)'$", init, re.MULTILINE)
version = match.group(1)

setuptools.setup(
    name='www',
    version=version,
    install_requires=[
        'Django==3.2.*',
        'dj-database-url',
        'gunicorn',
        'psycopg2-binary',
        'whitenoise',
    ],
)
