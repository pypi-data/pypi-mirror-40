# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['xmas']
entry_points = \
{'console_scripts': ['xmas = xmas:main']}

setup_kwargs = {
    'name': 'xmas',
    'version': '2018',
    'description': 'A cat, sitting on a wall, near a Xmas tree, is gazing starry picturesque night.',
    'long_description': '# Table of Contents\n\n\n\nMerry Christmas.\n\nHope you can have such a pleasant night, just as the cat sat on the wall near the Christmas tree, gazing at the picturesque starry night, of course, next to your lover.\n\n![img](./sshot.png)\n\n![img](./xmas.svg)\n',
    'author': 'Nasy',
    'author_email': 'nasyxx+git@gmail.com',
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
