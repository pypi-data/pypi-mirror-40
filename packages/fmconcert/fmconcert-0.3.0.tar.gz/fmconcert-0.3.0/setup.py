#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='fmconcert',
    version='0.3.0',
    description="Download France Musique concert file by scrapping on broadcast webpage",
    long_description=readme,
    author="Matthieu Boileau",
    author_email='matthieu.boileau@gmail.com',
    url='https://gitlab.com/boileaum/fmconcert',
    packages=[
        'fmconcert',
    ],
    package_dir={'fmconcert':
                 'fmconcert'},
    entry_points={
        'console_scripts': [
            'fmconcert=fmconcert.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='fmconcert',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
