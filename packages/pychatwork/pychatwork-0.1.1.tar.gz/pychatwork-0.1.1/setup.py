# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pychatwork']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'pychatwork',
    'version': '0.1.1',
    'description': "A Python wrapper for ChatWork's API",
    'long_description': "# pychatwork                                                              \n\nA Python wrapper for ChatWork's API\n\nhttp://developer.chatwork.com/\n\nチャットワークのAPIを簡単に使えるPythonのライブラリです。\n\n## Instollation\nInstall from PyPI.\n\n```\npip install pychatwork\n```\n\nInstall from github.\n\n```\npip install git+https://github.com/takeshi0406/pychatwork\n```\n\n## Usage\n\n``` python\nimport pychatwork as ch\n\nclient = ch.ChatworkClient('your access token')\n\n# get message from room 1234\nres = client.get_messages(room_id='1234', force=True)\n\n# post message to room 1234\nclient.post_messages(room_id='1234', message='hello chatwork!')\n```\n\n## TODO\n\nNow, only post message and get message methods were implemented.\n",
    'author': 'takeshi',
    'author_email': 'sci.and.eng@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
