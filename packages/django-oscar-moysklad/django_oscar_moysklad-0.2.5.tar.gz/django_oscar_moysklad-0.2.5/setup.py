import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


import os
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
    name='django_oscar_moysklad',
    version='0.2.5',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='Django oscar moysklad  support',
    long_description=README,
    url='https://github.com/initflow/django-oscar-moysklad',
    author='Pavel Pantiukhov',
    author_email='pantyukhov.p@gmail.com',
    install_requires=install_requires
)

