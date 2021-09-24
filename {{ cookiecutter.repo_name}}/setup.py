from setuptools import setup, find_packages
from pathlib import Path

SELF_PATH = Path(__file__).parent.absolute()


def read(path: Path):
    with open(path, 'r') as f:
        return f.read()

{%- set license_classifiers = {
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
} %}


setup(
    name='{{ cookiecutter.repo_name }}',
    description='',
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email='{{ cookiecutter.email }}',
    packages=find_packages(include=[
        'p01_Business_Question', 'p02_Data_Colection', 'p03_Data_Cleaning',
        'p04_Exploratory_Data_Analysis', 'p05_Feature_Engineering',
        'p06_Model_Selection', 'p07_Model_Evaluation', 'p08_Deployment'
    ]),
    include_package_data=True,
    install_requires=read(SELF_PATH / 'requirements/prod.txt').splitlines(),
{%- if cookiecutter.open_source_license in license_classifiers %}
    license="{{ cookiecutter.open_source_license }}",
{%- endif %}
    keywords='{{ cookiecutter.repo_name }}',
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}',
    long_description=read(SELF_PATH / 'README.md'),
)
