#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

import os
import sys
from distutils.core import setup
from setuptools import find_packages

__VERSION__ = "0.1"


def find_package_data_files(dirs):
    paths = []
    for directory in dirs:
        for (path, directories, filenames) in os.walk(directory):
            for filename in filenames:
                paths.append(os.path.join('..', path, filename))
    return paths


def setup_package():

    # Recursively gather all non-python module directories to be included in packaging.
    core_files = find_package_data_files([
        'django_project/static',
        'django_project/templates',
    ])

    setup(name='Quickstart-Secure-Django-Template',
        version=__VERSION__,
        description='A secure Oath2 enabled Django website with REST API',
        author='Robert Abram',
        author_email='rabram991@gmail.com',
        url='https://github.com/robabram/Quickstart-Secure-Django-Template',
        download_url='https://github.com/robabram/Quickstart-Secure-Django-Template/tarball/'+__VERSION__,
        packages=find_packages(exclude=['tests']),
        package_data={
            'django_project': core_files,
        },
        keywords=['template', 'security'],  # arbitrary keywords
        classifiers=[
            'Development Status :: 4 - Beta',
            'Programming Language :: Python',
            'Environment :: Console',
            'License :: MIT',
            'Operating System :: POSIX :: Linux',
        ],

        # Do not add additional requirements here, add them to requirements.in.
        install_requires=[
            'django',
        ],

        entry_points={
          'console_scripts': [],
        },

        tests_require=[
            'pytest',
            'pytest-runner',
            'pytest-pythonpath',
        ],
     )


if __name__ == "__main__":
    setup_package()
