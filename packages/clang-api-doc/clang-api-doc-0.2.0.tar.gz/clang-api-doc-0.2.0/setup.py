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
{'console_scripts': ['clang-api-check = clang_api_doc:clang_api_doc.check',
                     'clang-api-doc = clang_api_doc:clang_api_doc.main']}

setup_kwargs = {
    'name': 'clang-api-doc',
    'version': '0.2.0',
    'description': 'Automatically generate API documentation for C language dialects',
    'long_description': "clang-api-doc\n=============\n\nGenerate C API documentation using libclang Python bindings.\n\nFor an example see the [documentation](https://clang-api-doc.readthedocs.io).\n\n\nUsage\n-------------\n\nSimply call `clang-api-doc` once per file you wish to document, e.g.\n\n```bash\nclang-api-doc -f 'include/mylib/first.h' -o 'first.md'\nclang-api-doc -f 'include/mylib/second.h' -o 'second.md'\n```\n\nThese files can then be used in any way you wish to create your final documentation, for example\n- transform to a different format using `pandoc`\n- write an `index.md` file and use `sphinx` to create html docs\n\n\nInstallation\n-------------\n\nThe `clang-api-doc` package is on PyPI, so you can use `pip`, `poetry`, or whatever you like to install it.",
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
