# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['bookmarks_parser']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.5.0,<5.0.0', 'html5lib>=1.0,<2.0']

setup_kwargs = {
    'name': 'bookmarks-parser',
    'version': '0.1.2',
    'description': 'netscape bookmarks parser',
    'long_description': '# bookmarks-parser\n[![Build Status](https://travis-ci.org/andriyor/bookmarks-parser.svg?branch=master)](https://travis-ci.org/andriyor/bookmarks-parser)\n[![codecov](https://codecov.io/gh/andriyor/bookmarks-parser/branch/master/graph/badge.svg)](https://codecov.io/gh/andriyor/bookmarks-parser)\n[![image](https://img.shields.io/pypi/v/bookmarks-parser.svg)](https://pypi.org/project/bookmarks-parser/)\n[![image](https://img.shields.io/pypi/l/bookmarks-parser.svg)](https://pypi.org/project/bookmarks-parser/)\n[![image](https://img.shields.io/pypi/pyversions/bookmarks-parser.svg)](https://pypi.org/project/bookmarks-parser/)\n\nParsing Netscape bookmark (Google Chrome, Firefox, ... export files) .\n\n## Installation\n```\n$ pip install bookmarks-parser\n```\n\n## Usage\n```python\nimport pprint\nimport bookmarks_parser\n\nbookmarks = bookmarks_parser.parse("bookmarks.html")\npprint.pprint(bookmarks)\n```\n[output example](https://github.com/andriyor/bookmarks-parser/tree/master/tests/tests_data)\n\n## Development\nInstall [Poetry](https://poetry.eustace.io/docs/)   \n```\n$ poetry install\n```\nrun tests\n```\n$ poetry run pytest --cov=bookmarks_parser\n```\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)',
    'author': 'Andriy Orehov',
    'author_email': 'andriyorehov@gmail.com',
    'url': 'https://github.com/andriyor/amalgama-pq',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
