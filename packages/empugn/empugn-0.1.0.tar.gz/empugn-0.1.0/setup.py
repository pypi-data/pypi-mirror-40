#!/usr/bin/env python

import os
from setuptools import find_packages, setup


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='empugn',
    version='0.1.0',
    description='Generate HTML or XML from YAML or JSON',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author='Santtu Pajukanta',
    author_email='santtu@pajukanta.fi',
    url='http://github.com/japsu/empugn',
    packages=find_packages(exclude=["tests"]),
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'empugn = empugn.__main__:main',
        ]
    },
    install_requires=["yattag~=1.10.1"],
    tests_require=["pytest", "emrichen"],
    setup_requires=["pytest-runner"],
    extras_require={
        'yaml': ['PyYAML'],
        'emrichen': ['emrichen'],
    }
)
