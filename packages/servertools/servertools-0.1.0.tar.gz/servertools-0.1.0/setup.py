#!/usr/bin/env python
# @formatter:off
#
#                                             ,,
#                                             db
#     \
#     _\,,          `7MM  `7MM  `7MMpMMMb.  `7MM  ,p6"bo   ,pW"Wq.`7Mb,od8 `7MMpMMMb.
#    "-=\~     _      MM    MM    MM    MM    MM 6M'  OO  6W'   `Wb MM' "'   MM    MM
#       \\~___( ~     MM    MM    MM    MM    MM 8M       8M     M8 MM       MM    MM
#      _|/---\\_      MM    MM    MM    MM    MM 8M       8M     M8 MM       MM    MM
#     \        \      MM    MM    MM    MM    MM YM.    , YA.   ,A9 MM       MM    MM
#                     `Mbod"YML..JMML  JMML..JMML.YMbmd'   `Ybmd9'.JMML.   .JMML  JMML.
#
#                     <> with ❤ by Micha Grandel (talk@michagrandel.de)
#                     
#                     Project:         https://github.com/michagrandel/servertools
#                     Report a bug:    https://github.com/michagrandel/servertools/issues
#                     Contribute:      https://github.com/michagrandel/servertools/wiki/Contribute
#                     
#                     -----------------------------------------------------------------
#                     
#                     Copyright 2019 Micha Grandel
#                     
#                     Licensed under the Apache License, Version 2.0 (the 'License');
#                     you may not use this file except in compliance with the License.
#                     You may obtain a copy of the License at
#                     
#                     http://www.apache.org/licenses/LICENSE-2.0
#                     
#                     Unless required by applicable law or agreed to in writing,
#                     software distributed under the License is distributed on an
#                     'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
#                     either express or implied. See the License for the specific
#                     language governing permissions and limitations under the License.
#
#                     -----------------------------------------------------------------
#                     @formatter:on

""":mod:`setup.py` -- A setuptools based setup module for Server-Tools


.. module:: setup.py
   :platform: Unix, Windows
   :synopsis: A setuptools based setup module for Server-Tools
.. moduleauthor:: Micha Grandel <talk@michagrandel.de>

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from __future__ import unicode_literals, print_function
from io import open
from typing import *
import os
import glob


try:
    from setuptools import setup, find_packages
    packages = find_packages(exclude=['contrib', 'docs', 'tests'])
except ImportError:
    from distutils.core import setup
    from pkgutil import walk_packages
    import servertools
    
    
    def find_packages(path: AnyStr = __path__, prefix: AnyStr = "") -> None:
        """
        find packages that are included in this project
        
        :param path: start directory to search for packages (usually the project directory)
        :param prefix: prefix for recursion
        :return: list with packages in this project
        """
        yield prefix
        prefix = prefix + "."
        for _, name, ispkg in walk_packages(path, prefix):
            if ispkg:
                yield name
    
    
    packages = list(find_packages('.', 'ServerTools'))

__status__ = 'alpha'
__author__ = 'Micha Grandel'
__maintainer__ = 'Micha Grandel'
__version__ = '0.1.0'
__copyright__ = '<> with ❤ by Micha Grandel'
__license__ = 'Apache License, Version 2.0'
__contact__ = 'talk@michagrandel.de'
__maintainer_contact__ = 'talk@michagrandel.de'

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'Readme.md'), encoding='utf-8') as f:
    long_description = f.read()

def requirements(category: AnyStr = 'install') -> Union[List[AnyStr], AnyStr]:
    """
    extract requirements from requirements.txt
    
    :param category: 'install', 'dev' or 'test' for requirements, dev-requirements or test-requirements
    :return: list with requirements 
    """
    if category.lower().startswith('install'):
        file_ = 'requirements.txt'
    elif category.lower().startswith('dev'):
        file_ = 'development-requirements.txt'
    elif category.lower().startswith('test'):
        file_ = 'test-requirements.txt'
    else:
        return []
    
    try:
        with open(file_, 'r', encoding='utf-8') as requirements_file:
            content = requirements_file.read()
        content = content.split('\n')
    except (IOError, OSError) as error:
        content = []
    
    return content


setup(
    name='servertools',
    version=__version__,
    description='administration tools for specific servers',
    long_description=long_description,
    url='https://github.com/michagrandel/servertools',
    author=__author__,
    author_email=__contact__,
    maintainer=__maintainer__,
    maintainer_email=__maintainer_contact__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: Apache Software License',
        # 'License :: Other/Proprietary License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: Microsoft',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        'Natural Language :: German',
    ],
    keywords='server admin tools',
    packages=packages,
    install_requires=requirements(),
    extras_require={
        'dev': requirements('dev'),
        'test': requirements('test'),
    },
    package_data={
        # translations
        'servertools': ['data/i18n/*/LC_MESSAGES/*.mo'],
    },
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'server-tools=scripts.server_tools:main',
        ],
    },
    download_url='https://github.com/michagrandel/servertools/archive/v0.1.tar.gz',
    # scripts=['script/server-tools.py']  # [os.path.join('script', x) for x in os.listdir('script')]
)
