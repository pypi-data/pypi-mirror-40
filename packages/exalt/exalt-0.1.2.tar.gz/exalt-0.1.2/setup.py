# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['exalt']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'exalt',
    'version': '0.1.2',
    'description': 'Namespace promotion done right!',
    'long_description': '<p align="center">\n\t<img src="https://user-images.githubusercontent.com/9287847/50569701-4cf0f680-0d6c-11e9-93d9-f7c57983fc17.png"/ width="450" alt="exalt">\n</p>\n\n---\n\n[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://python.org)\n![Not production ready](https://img.shields.io/badge/production%20ready-not%20really-red.svg)\n![Travis status](https://travis-ci.org/PhilipTrauner/exalt.svg?branch=master)\n\n**exalt** provides a convenient way to dynamically create closures and bind them to a custom namespace. This is primarily useful for preserving an execution-context when calling into a different function.\n\n## Example\n\n```python\nfrom exalt import promote\n\n\ndef baz():\n    return bar\n\n\ndef foo():\n    bar = "baz"\n\n    return promote(baz, **locals())()\n\n\nprint(foo())\n```\n<p align="center">——————————————————————————— ↓ ———————————————————————————</p>\n\n```\nbaz\n```\n\n## Installation\n```bash\npip3 install --user exalt\n```\n\n## Disclaimer\n**exalt** heavily relies on CPython implementation details and probably shouldn\'t be used in a production environment.\n',
    'author': 'Philip Trauner',
    'author_email': 'philip.trauner@arztpraxis.io',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
