# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['xgit']

package_data = \
{'': ['*'], 'xgit': ['gitignore/*']}

install_requires = \
['requests>=2.21,<3.0']

entry_points = \
{'console_scripts': ['xgit = xgit.__main__:main']}

setup_kwargs = {
    'name': 'xgit',
    'version': '0.1.3',
    'description': 'An opinionated command line tools to make your life easier with Git and Gitignore',
    'long_description': '# xgit\n\nAn opinionated command line tools to make your life easier with Git and Gitignore\n\n## Installation\n\nInstall as global from pip.\n\n```\npip3 install xgit\n```\n\nOr clone the repo, and install from the clone (and you may also edit as you wish).\n\n```\ngit clone https://github.com/patarapolw/xgit.git\npip3 install -e xgit\n```\n\n## Usage\n\n```\n$ xgit -h\nAcceptable commands:\nxgit init           Initialize new git along with .gitignore\nxgit commit message Commit to git with the following message\nxgit cpush message  Commit and push to git with the following message\nxgit gi             Generate gitignore from files in the directory\nxgit push           Push changes to origin\nxgit                Prompt for choices\n```\n\n```\n$ xgit\nWhat do you want to do?\n1. Initialize Git\n2. Commit current changes\n3. Commit current changes and push to remote\n4. Generate and commit .gitignore\n5. Push to remote\nPlease select [1-5]:\n```\n\n## Note\n\n- `.gitignore` is generated from <https://www.gitignore.io/>, but this project also allows me to generate a custom `.gitignore` based on [/xgit/gitignore/](/xgit/gitignore/).\n- To learn more about my experience with Git, see <https://github.com/patarapolw/SimpleGit>\n',
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/xgit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
