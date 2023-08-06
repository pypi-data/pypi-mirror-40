# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from io import open
from os import path

from setuptools import setup


HERE = path.dirname(path.abspath(__file__))

with open(path.join(HERE, 'README.md'), 'r', encoding='utf-8') as f:
    README = f.read()


setup(
    name='datadog-a7',
    version="0.0.4",

    description='The Datadog Checks Shared Tools',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords='datadog agent checks shared tools',

    url='https://github.com/DataDog/datadog-checks-shared',
    author='Datadog',
    author_email='packages@datadoghq.com',
    license='BSD',

    # See https://pypi.org/classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    packages=['a7'],
    install_requires=['pylint'],
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'a7_validate = a7:main',
        ],
    },
)
