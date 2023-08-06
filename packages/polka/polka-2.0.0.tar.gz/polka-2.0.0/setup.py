# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['polka']
setup_kwargs = {
    'name': 'polka',
    'version': '2.0.0',
    'description': 'A module provides access to the public Polka API. (https://polka.academy/).',
    'long_description': '',
    'author': 'Dima Koskin',
    'author_email': 'dmksknn@gmail.com',
    'url': 'https://github.com/dmkskn/polka/',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
