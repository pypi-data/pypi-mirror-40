"""

ec2tools :  Copyright 2018, Blake Huber

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

see: https://www.gnu.org/licenses/#GPL

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
contained in the program LICENSE file.

"""

import os
import sys
from setuptools import setup, find_packages
from codecs import open
import ec2tools


requires = [
    'boto3>=1.7.1',
    'botocore>=1.10.1',
    'pyaws>=0.2.24',
    'Pygments>=2.2.0',
    'VeryPrettyTable'
]


def read(fname):
    basedir = os.path.dirname(sys.argv[0])
    return open(os.path.join(basedir, fname)).read()


setup(
    name='ec2tools',
    version=ec2tools.__version__,
    description='Scripts & Tools for use with Amazon Web Services EC2 Service',
    long_description=read('DESCRIPTION.rst'),
    url='https://github.com/fstab50/ec2tools',
    author=ec2tools.__author__,
    author_email=ec2tools.__email__,
    license='Apache',
    classifiers=[
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows'
    ],
    keywords='aws amazon amazonlinux redhat centos ami tools',
    packages=find_packages(exclude=['docs', 'scripts', 'assets']),
    install_requires=requires,
    python_requires='>=3.6, <4',
    entry_points={
        'console_scripts': [
            'machineimage=ec2tools.current_ami:init_cli',
            'profileaccount=ec2tools.environment:init_cli',
            'runmachine=ec2tools.launcher:init_cli',
        ]
    },
    zip_safe=False
)
