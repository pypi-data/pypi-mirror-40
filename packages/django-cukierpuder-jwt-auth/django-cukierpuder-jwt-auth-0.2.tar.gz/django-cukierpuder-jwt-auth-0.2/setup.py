import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-cukierpuder-jwt-auth',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    license='GNU',
    description='A simple authorization Django app based on JSON Web Tokens.',
    long_description=README,
    url='https://github.com/CukierPuder/django-cukierpuder-jwt-auth',
    download_url='https://github.com/CukierPuder/django-cukierpuder-jwt-auth/archive/v0.2.tar.gz',
    author='CukierPuder',
    author_email='cukier_puder@hotmail.com',
    install_requires=[
        'Django',
        'djangorestframework',
        'djangorestframework-simplejwt',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
