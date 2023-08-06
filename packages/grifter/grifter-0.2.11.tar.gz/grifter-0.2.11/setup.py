import os
from setuptools import setup, find_packages


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name), 'r') as f:
        return f.read()


setup(
    name='grifter',
    version=read('VERSION'),
    author='Brad Searle',
    author_email='bradleysearle@gmail.com',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    description="A package to generate Vagrantfiles for use with Vagrant.",
    long_description=read('README.md'),

    include_package_data=True,
    packages=find_packages(),

    install_requires=[
        'jinja2',
        'pyyaml',
        'click',
        'cerberus',
    ],

    entry_points={
        'console_scripts': [
            'grifter = grifter:cli',
        ]
    },

)
