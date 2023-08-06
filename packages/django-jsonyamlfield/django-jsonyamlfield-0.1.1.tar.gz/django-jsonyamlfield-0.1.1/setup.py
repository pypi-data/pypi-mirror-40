#!/usr/bin/env python

import os
from setuptools import setup, find_packages

setup(
    name = "django-jsonyamlfield",
    version = "0.1.1",
    description='Django JSONField as YAML.',
    url = 'https://gitlab.com/mike_tk/django-jsonyamlfield',
    long_description="""Same as Django JSONField but represent it as YAML""",
    author = 'Mike Tkachuk',
    author_email = 'mike@tkachuk.name',
    packages = find_packages(),
    install_requires=[
      'pyyaml',
    ]
)