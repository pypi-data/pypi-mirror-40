# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['stylo',
 'stylo.color',
 'stylo.design',
 'stylo.domain',
 'stylo.domain.transform',
 'stylo.image',
 'stylo.math',
 'stylo.shape',
 'stylo.testing',
 'stylo.time']

package_data = \
{'': ['*']}

install_requires = \
['Pillow', 'click', 'numpy', 'tqdm']

extras_require = \
{'jupyter': ['matplotlib', 'jupyter>=1.0,<2.0'],
 'testing': ['hypothesis', 'pytest==4.0.2']}

setup_kwargs = {
    'name': 'stylo',
    'version': '0.9.3',
    'description': 'Drawing images with a blend of Python and Mathematics',
    'long_description': '# Stylo\n|   |   |\n|:-------------:|----|\n| **Project** | ![MIT License](https://img.shields.io/github/license/alcarney/stylo.svg) [![Gitter](https://badges.gitter.im/stylo-py/Lobby.svg)](https://gitter.im/stylo-py/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) |\n| **Docs** | [![Documentation Status](https://readthedocs.org/projects/stylo/badge/?version=latest)](https://stylo.readthedocs.io/en/latest/?badge=latest)|\n| **Code**| [![Travis](https://travis-ci.org/alcarney/stylo.svg?branch=develop)](https://travis-ci.org/alcarney/stylo) [![Coveralls](https://coveralls.io/repos/github/alcarney/stylo/badge.svg?branch=develop)](https://coveralls.io/github/alcarney/stylo?branch=develop) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)|\n| **PyPi** | [![PyPi Version](https://img.shields.io/pypi/v/stylo.svg)](https://pypi.org/project/stylo) [![PyPi Supported Versions](https://img.shields.io/pypi/pyversions/stylo.svg)](https://pypi.org/project/stylo)|\n\n**Stylo is in early development, while it is useable we cannot make any\nstability guarantees.**\n\nStylo is a Python library that allows you to create images and animations\npowered by your imagination and a little mathematics. While mathematics is very\nmuch at the core you do not have to be a mathematician to use it!\n\nFor example here is a simple image of a boat that can be made with just a few\nlines of Python\n\n\n![A Boat](https://raw.githubusercontent.com/alcarney/stylo/develop/img/a-boat.png)\n\n\n```python\nimport stylo as st\n\n# Let\'s define the shapes we want to draw\nsun = st.Circle(-7, 3.4, 1.5, fill=True)\nsea = st.Circle(0, -55, 55, fill=True)\nsails = st.Triangle((0.1, 0.6), (2.5, 0.6), (0.1, 3.5)) | st.Triangle((-0.1, 0.6), (-1.5, 0.6), (-0.1, 3.5))\nboat = st.Rectangle(0, 0, 3.5, 1) | st.Triangle((1.75, -0.5), (1.75, 0.5), (2.25, 0.5))\nmast = st.Rectangle(0, 2, 0.125, 3)\n\n# Move some into position\nboat = boat >> st.translate(0, -2)\nsails = sails >> st.translate(0, -2)\nmast = mast >> st.translate(0, -2)\n\n# Finally let\'s bring it all together\nimage = st.LayeredImage(background="99ddee", scale=8)\n\nimage.add_layer(sun, "ffff00")\nimage.add_layer(sea, "0000ff")\nimage.add_layer(boat, "dd2300")\nimage.add_layer(mast, "000000")\nimage.add_layer(sails, "ffffff")\n\nimage(1920, 1080, filename="a-boat.png")\n```\n\n## Installation\n\nStylo is available for Python 3.5+ and can be installed using Pip:\n\n```sh\n$ pip install stylo\n```\n\nBe sure to check out the [documentation](https://alcarney.github.io/stylo)\n(under construction) for details on how to get started with stylo.\n\n## Contributing\n\nContributions are welcome! Be sure to checkout the\n[Contributing](https://alcarney.github.io/stylo/contributing/) section of the\ndocumentation to get started.\n\n**Note:** While `stylo` itself supports Python 3.5+, due to some of the\ndevelopment tools we use you need to have Python 3.6+ in order to contribute\n**code** to the library. Other versions of Python work just as well if you are\nlooking to contribute documentation.\n',
    'author': 'Alex Carney',
    'author_email': 'alcarneyme@gmail.com',
    'url': 'https://stylo.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
