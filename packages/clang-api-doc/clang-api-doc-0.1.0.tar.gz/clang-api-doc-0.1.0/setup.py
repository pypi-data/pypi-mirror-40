# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': '.'}

packages = \
['clang_api_doc']

package_data = \
{'': ['*']}

install_requires = \
['clang']

entry_points = \
{'console_scripts': ['clang-api-doc = clang_api_doc:clang_api_doc.main']}

setup_kwargs = {
    'name': 'clang-api-doc',
    'version': '0.1.0',
    'description': 'Automatically generate API documentation for C language dialects',
    'long_description': 'clang-api-doc\n=============\n\nGenerate C/C++ API documentation using libclang Python',
    'author': 'Gideon Müller',
    'author_email': 'gpmueller@outlook.com',
    'url': 'https://github.com/gpmueller/clang-api-doc',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
