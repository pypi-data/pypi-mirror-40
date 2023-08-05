# pylint: disable=W0622
"""cubicweb-wireit application packaging information"""

modname = 'wireit'
distname = 'cubicweb-wireit'

numversion = (0, 6, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'WireIt workflow store for the CubicWeb framework'
web = 'http://www.cubicweb.org/project/%s' % distname

__depends__ = {'cubicweb': '>= 3.16.0',
               'six': '>= 1.4.0',
               'cubicweb-file': None}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]

