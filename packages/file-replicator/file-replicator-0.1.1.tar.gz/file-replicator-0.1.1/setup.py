# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['file_replicator']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'inotify>=0.2.10,<0.3.0']

entry_points = \
{'console_scripts': ['file-replicator = file_replicator.cli:main']}

setup_kwargs = {
    'name': 'file-replicator',
    'version': '0.1.1',
    'description': 'Replicate files to another computer for remote development',
    'long_description': '# File Replicator\n\nReplicate files one-way to another computer e.g. for remote development.\n\nA key use-case is to keep in sync a directory of development files from a computer on which\nthe files are edited with a copy of those files in a docker container running on a remote docker host.\n\nDependencies are:\n* Python and some Python packages on the development machine\n* Ability to run bash (including busybox) on the remote machine with connected `stdin`\n\nNothing is installed remotely.\n\nThis has only been tested between two Linux machines.\n\n# How it works\n\nThe approach is to run a small bash program on the remote end which is able to add/update new files in\n(potentially) new directories. It receives commands over `stdin`, endlessly waiting for:\n* an absolute path to a filename\n* a newline\n* an integer number of bytes\n* a newline\n* that many bytes of data\n* ...repeat...\n\nThe controlling end then simply sends files over to the `stdin` of the receiving bash program.\nEstablishing the connection to the remote end is outside the remit of this tool. Instead it accepts\nas an argument the command to make such a connection. See examples below.\n\nIt has two key operations:\n\n1. recursively walking a source tree of files and sending them over the wire to the destination\n2. watching for changes or new files and directories before sending them over the wire to the destination\n\nSo there is no "difference algorithm" like rsync, no attempt to compress, the connection is made\nentirely using standard means like ssh and docker, no ports to open, and even the bash program\non the remote end is sent over every time so nothing is installed remotely.\n\nThis is sufficient for editing code on a local computer and automatically replicating to a remote server\nor docker container.\n\n# Usage and examples\n\nSee help:\n\n    TODO update help\n\nReplicate files from local directory `my_project` to directory `/home/code/my_project` on\nremote machine called `my.server.com`:\n\n    file-replicator my_project /home/code ssh my.server.com bash\n\nTo replicate files from local directory `my_project` to directory `/home/code/my_project` in a\nrunning docker container called `my_container` on a potentially remote host (depending upon the `DOCKER*`\nenvironment variables e.g. as set by `docker-machine eval`):\n\n    file-replicator my_project /home/code -- docker exec -i my_container bash\n\nOr to do the same but using `docker-compose` instead:\n\n    file-replicator my_project /home/code -- docker-compose exec -T my_container bash\n\n# Limitations\n\nDue to limitations with inotify (race conditions around watching for changes in newly created directories), it\nis possible that the watching-for-changes phase becomes out of step. In which case, just restart the whole program.\n(the tool includes some self-restarting behaviour, but ultimately a full restart may sometimes be needed).\n\nInformation printed to stdout indicates when this happens.\n\n# Tests\n\nTODO copy and paste\n\n# Contributions\n\nPull-requests welcome. Please considering including tests.\n\nThe package is maintained using poetry (https://poetry.eustace.io) and pyenv (https://github.com/pyenv/pyenv).\n\nThe code is formatted using black (https://black.readthedocs.io/en/stable).\n\nIt is tested using pytest (`poetry run pytest`). Note that in order to run these tests the current user\nmust be able to ssh to localhost without a password.\n\n# Commit checklist\n\n1. check version both in `pyproject.toml` and `file_replicator/__init__.py`\n1. check git tag\n1. isort -rc .\n1. black .\n1. pytest -v\n1. update this README.md with the latest output from the tests\n1. update this README.md with the latest output from the --help option\n\n# TODO\n\nAdd option to exclude certain files\nAdd docs to show an example output. Possibly a screenshot so it looks nice.\nPublish on Pypi. (check copyright etc)',
    'author': 'Timothy Corbett-Clark',
    'author_email': 'timothy.corbettclark@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
