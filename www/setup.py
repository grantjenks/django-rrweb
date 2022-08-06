import setuptools

setuptools.setup(
    name='www',
    version=todo,
    install_requires=[
        'Django=3.2.*',
        'dj-database-url',
        'gunicorn',
        'psycopg2-binary',
        'whitenoise',
    ],
)
