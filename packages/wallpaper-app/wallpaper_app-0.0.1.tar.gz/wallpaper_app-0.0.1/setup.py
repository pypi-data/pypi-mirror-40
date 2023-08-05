# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['wallpaper_app']

package_data = \
{'': ['*']}

install_requires = \
['pync>=2.0,<3.0', 'requests>=2.21,<3.0', 'rumps>=0.2.2,<0.3.0']

entry_points = \
{'console_scripts': ['wallpaper_app = wallpaper_app:launch_app']}

setup_kwargs = {
    'name': 'wallpaper-app',
    'version': '0.0.1',
    'description': 'A macOS statusbar app for wallpaper switching',
    'long_description': '# wallpaper_app\n\n\n## Installation\n\n```bash\n$ pip install wallpaper_app\n```\n\n\n## Usage\n\nExecuting\n\n```bash\n$ wallpaper_app\n```\n\nwill spawn a statusbar app with controls.\n',
    'author': 'kpj',
    'author_email': 'kpjkpjkpjkpjkpjkpj@gmail.com',
    'url': 'https://github.com/kpj/wallpaper_app',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
