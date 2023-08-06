# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['twilog_web_archiver']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'click>=7.0,<8.0',
 'lxml>=4.3,<5.0',
 'requests>=2.21,<3.0',
 'savepagenow>=0.0.12,<0.0.13']

entry_points = \
{'console_scripts': ['twilog-web-archiver = twilog_web_archiver.main:main']}

setup_kwargs = {
    'name': 'twilog-web-archiver',
    'version': '0.1.0.post2',
    'description': 'Save month list pages of twilog.org by using archive.org.',
    'long_description': 'twilog-web-archiver\n===================\n\nSave month list pages of twilog.org by using archive.org.\n\nRequirement\n-----------\n\n- :code:`Python >= 3.6`\n\nInstall\n-------\n\n.. code-block:: bash\n\n    $ pip install twilog-web-archiver\n\nUsage\n-----\n\n.. code-block:: bash\n\n    $ twilog-web-archiver SCREEN_NAME\n',
    'author': 'TAKAHASHI Shuuji',
    'author_email': 'shuuji3@gmail.com',
    'url': 'https://github.com/shuuji3/twilog-web-archiver',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
