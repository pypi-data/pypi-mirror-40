# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['poetrify']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.7.2,<0.8.0', 'licensename>=0.4.2,<0.5.0', 'tomlkit>=0.5.3,<0.6.0']

entry_points = \
{'console_scripts': ['poetrify = poetrify.cli:application.run']}

setup_kwargs = {
    'name': 'poetrify',
    'version': '0.2.1',
    'description': 'Pipfile to pyproject.toml for Poetry',
    'long_description': '# Poetrify\n\nPipfile to pyproject.toml for Poetry.\n\n```\n$ git clone https://github.com/kk6/poetrify.git\n$ cd poetrify\n$ poetry install\n$ poetry run poetrify generate -w /path/to/workspace\n```\n\nor\n\n```\n$ git clone https://github.com/kk6/poetrify.git\n$ cd poetrify\n$ poetry build\n$ pip install --user ./dist/poetrify-0.2.1-py3-none-any.whl\n$ cd path/to/workspace\n$ poetrify generate\n```\n\n## required\n\n- `poetry` command (See: https://poetry.eustace.io/docs/#installation )\n',
    'author': 'kk6',
    'author_email': 'hiro.ashiya@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
