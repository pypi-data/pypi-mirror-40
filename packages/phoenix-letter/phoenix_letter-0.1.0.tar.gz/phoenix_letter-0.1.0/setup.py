import codecs
import os
import re
from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def parse_requirements_file():
    with open("requirements.txt", "r") as file:
        lines = file.readlines()
        return [item.split("==")[0] for item in lines]


setup(
    name='phoenix_letter',
    version=find_version("src", "phoenix_letter", "version.py"),
    url='https://github.com/renanvieira/phoenix-letter',
    license='MIT',
    author='Renan Vieira',
    author_email='me@renanvieira.net',
    package_dir={'phoenix_letter': 'src/phoenix_letter'},
    packages=find_packages('src'),
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    description='CLI to move messages from a AWS SQS Queue to another',
    keywords=['AWS', 'SQS', 'Queue', 'DLQ', "Dead", "Letter", "Queue"],
    python_requires='>=2.7',
    zip_safe=False,
    entry_points={
        'console_scripts': ['phoenix_letter=phoenix_letter.main:main']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    install_requires=parse_requirements_file()
)
