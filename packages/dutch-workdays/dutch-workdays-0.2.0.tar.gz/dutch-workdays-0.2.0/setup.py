# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dutch_workdays']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dutch-workdays',
    'version': '0.2.0',
    'description': 'A very small library that handles with Dutch calendars and holidays 🇳🇱',
    'long_description': 'Dutch Workdays\n==============\n\nA very small library that handles with Dutch calendars and holidays 🇳🇱\n\nInstalling\n----------\n\n.. code-block:: bash\n\n    pip install dutch-workdays\n\nUsage\n-----\n\n.. code-block:: python\n\n    >>> from dutch_workdays import Calendar\n    >>> cal = Calendar()\n    >>> cal.get_king_queen_day(2018)\n    (datetime.date(2018, 4, 27), "King\'s day")\n\n\n``dutch-workdays`` works as a drop-in replacement of workalendar_, so for the rest of the API please refer to\nthe `workdays documentation`_.\n\nWhy not just using Workalendar instead?\n---------------------------------------\n\nWorkalendar is an awesome library, it\'s very complete and very well maintained but it\'s, unfortunately, quite a big dependency as well. It not only includes Python code to handle calendars from most of the world, but it also requires C libraries to calculate high-precision astronomy computations. It\'s an overkill if you only need to know about Dutch holidays.\n\nDiffences from Workalendar\n--------------------------\n\n- All the codebase is type annotated.\n- Zero dependencies\n- Dateutil easter calculation is vendorized.\n    \n.. _workalendar: https://github.com/peopledoc/workalendar\n.. _workdays documentation: https://peopledoc.github.io/workalendar/\n',
    'author': 'New10',
    'author_email': 'pypi-admin@new10.com',
    'url': 'https://gitlab.com/new10-public/dutch-workdays/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
