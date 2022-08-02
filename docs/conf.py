# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import pathlib
import sys
import django

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'tests'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'
django.setup()
from django_rrweb import __author__, __copyright__, __title__, __version__

project = __title__
copyright = __copyright__
author = __author__
release = __version__


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'

html_theme_options = {
    'logo': 'gj-logo.png',
    'logo_name': True,
    'logo_text_align': 'center',
    'travis_button': False,
    'analytics_id': 'UA-19364636-2',
    'show_powered_by': False,
    'github_user': 'grantjenks',
    'github_repo': 'django-rrweb',
    'github_type': 'star',
}

html_static_path = ['_static']

html_sidebars = {
    '**': [
        'about.html',
        'gumroad.html',
        'localtoc.html',
        'relations.html',
        'searchbox.html',
    ]
}
