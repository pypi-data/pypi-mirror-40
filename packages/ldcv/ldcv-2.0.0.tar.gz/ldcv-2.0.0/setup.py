# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

modules = \
['ldcv']
install_requires = \
['lxml>=4.2,<5.0']

entry_points = \
{'console_scripts': ['ldcv = ldcv:main']}

setup_kwargs = {
    'name': 'ldcv',
    'version': '2.0.0',
    'description': 'LangMan Console Version',
    'long_description': '============\nldcv |Build|\n============\n\nA console version LongMan_ dictionary.\n\n\nUsage\n-----\n\n.. code-block:: text\n\n   usage: ldcv [-h] [-f] [-j] [--cache CACHE] [-c CONFIG]\n               [--color {always,auto,never}]\n               [words [words ...]]\n\n   LongMan Console Version\n\n   positional arguments:\n     words                 words or quoted phrases to lookup\n\n   optional arguments:\n     -h, --help            show this help message and exit\n     -f, --full            print verbose explanations. Default to print first\n                           three explanations\n     -j, --json            dump the explanation with JSON style\n     --cache CACHE         specify a word list file then cache words from it to\n                           <cachefile>\n     -c CONFIG, --config CONFIG\n                           specify a config file\n     --color {always,auto,never}\n                           colorize the output. Default to "auto" or can be\n                           "never" or "always"\n\n\nInstallation\n------------\n\n.. code-block:: shell\n\n   $ pip install ldcv\n\n\nEnviroment or dependences\n-------------------------\n\n- Python (3.x)\n- lxml_\n\n\nThanks\n------\n\n- ydcv_\n\n.. _LongMan: https://www.ldoceonline.com/\n.. _ydcv: https://github.com/felixonmars/ydcv\n.. _lxml: https://lxml.de/\n.. |Build| image:: https://img.shields.io/badge/build_with-poetry-pink.svg?style=flat-square&logo=appveyor\n   :target: https://github.com/sdispater/poetry\n',
    'author': 'leetking',
    'author_email': 'li_tking@163.com',
    'url': 'https://github.com/leetking/ldcv',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
