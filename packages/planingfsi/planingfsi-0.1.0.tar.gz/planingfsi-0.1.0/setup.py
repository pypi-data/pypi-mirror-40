# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['planingfsi', 'planingfsi.fe', 'planingfsi.fsi', 'planingfsi.potentialflow']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'krampy',
 'matplotlib>=3.0,<4.0',
 'numpy>=1.15,<2.0',
 'pytest-runner>=4.2,<5.0',
 'scipy>=1.2,<2.0',
 'six>=1.12,<2.0']

entry_points = \
{'console_scripts': ['generateMesh = planingfsi:cli.mesh.main',
                     'planingFSI = planingfsi:cli.planingfsi.main']}

setup_kwargs = {
    'name': 'planingfsi',
    'version': '0.1.0',
    'description': 'Fluid-Structure Interaction for large deformation planing surfaces',
    'long_description': '# PlaningFSI\n\n[![image](https://img.shields.io/pypi/v/planingfsi.svg)](https://pypi.org/project/planingfsi/)\n[![image](https://img.shields.io/pypi/l/planingfsi.svg)](https://pypi.org/project/planingfsi/)\n\n## Cautionary Note\n\nI am currently working on releasing this package as open source.\nSince this is my first open-source release, the next few releases on PyPi should not be used for production.\nI will release version 1.0.0 once I feel that I have sufficiently cleaned up and documented the code. \n\n## Summary\n\nPlaningFSI is a scientific Python program use to calculate the steady-state response of 2-d marine structures subject to planing flow with consideration for Fluid-Structure Interaction (FSI) as well as rigid body motion.\nIt was originally written in 2012-2013 to support my Ph.D. research and has recently (2018) been updated and released as open source.\n\n## Required Python version\n\nThe code is written in Python and was originally written in Python 2.6.5.\nit has since been updated to require Python 3.6+.\nAlthough future versions of Python **should** support, the code, I can make no guarantees.\n\nThe code requires several Python modules, which are imported at the top of each program file. All of the modules should be included with the standard installation of Python except for the following:\n- Numpy (provides support for array structures and other tools for numerical analysis)\n- Scipy (provides support for many standard scientific functions, including interpolation)\n- Matplotlib (provides support for plotting)\n\n\n## Installation\n\nPlaningFSI can be installed with pip:\n\n```\npip insall planingfsi\n```\n',
    'author': 'Matt Kramer',
    'author_email': 'matthew.robert.kramer@gmail.com',
    'url': 'https://bitbucket.org/mattkram/planingfsi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
