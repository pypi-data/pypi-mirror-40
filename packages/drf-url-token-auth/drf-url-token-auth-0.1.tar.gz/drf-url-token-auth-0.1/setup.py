import os
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(HERE, 'README.md')).read()

setup(
    name='drf-url-token-auth',
    version='0.1',
    packages=['drf_url_token_auth'],
    description=
    'Authentication scheme for django rest framework that allow to use token in a url',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Develatio Technologies S.L.',
    author_email='contacto@develat.io',
    url='https://github.com/develatio/drf-url-token-auth/',
    license='MIT',
    install_requires=[
        'Django>=2.0',
    ])
