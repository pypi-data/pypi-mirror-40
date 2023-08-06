# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['pipfile_requirements']
install_requires = \
['requirementslib>=1.3,<2.0']

entry_points = \
{'console_scripts': ['pipfile2req = pipfile_requirements:main']}

setup_kwargs = {
    'name': 'pipfile-requirements',
    'version': '0.1.0.post0',
    'description': 'A CLI tool to covert Pipfile/Pipfile.lock to requirments.txt',
    'long_description': "# pipfile-requirements\nCLI tool to covert Pipfile/Pipfile.lock to requirments.txt\n\n[![Build Status](https://travis-ci.org/frostming/pipfile-requirements.svg?branch=master)](https://travis-ci.org/frostming/pipfile-requirements)\n[![](https://img.shields.io/pypi/v/pipfile-requirements.svg)](https://pypi.org/project/pipfile-requirements)\n[![](https://img.shields.io/pypi/pyversions/pipfile-requirements.svg)](https://pypi.org/project/pipfile-requirements)\n\n## Required Python version\n\n`>=2.7, >=3.4`\n\n## What does it do?\n\nThe tool is built on top of [requirementslib][https://github.com/sarugaku/requirementslib] to provide a simple CLI to\nconvert the Pipenv-managed files to requirements.txt.\n\nPipenv is a great tool for managing virtualenvs and dependencies, but it may be not that useful in deployment.\nPip installation is much faster than Pipenv manipulation, since the latter needs extra requests to PyPI for hash checking.\nInstalling a Pipenv in deployment may be overkilled. We just need a requirements.txt to tell CI or production server\nwhich packages and versions should be installed.\n\n\n## Installation\n\n```bash\n$ pip install pipfile-requirements\n```\n\nAn executable named `pipfile2req` will be ready for use in the bin path.\n\n## Usage:\n\n```\n$ pipfile2req --help\nusage: pipfile2req [-h] [-p PROJECT] [--hashes] [-d] [file]\n\npositional arguments:\n  file                  The file path to covert, support both Pipfile and\n                        Pipfile.lock. If it isn't given, will try Pipfile.lock\n                        first then Pipfile.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -p PROJECT, --project PROJECT\n                        Specify another project root\n  --hashes              whether to include the hashes\n  -d, --dev             whether to choose the dev-dependencies section\n```\n\n## License\n\n[MIT](/LICENSE)\n\n## Others\n\nIt is my first time to use Poetry to manage my project, related to Pipenv, lol.\n",
    'author': 'Frost Ming',
    'author_email': 'mianghong@gmail.com',
    'url': 'https://github.com/frostming/pipfile-requirements',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
