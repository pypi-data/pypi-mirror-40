# pylint: disable=W0622
"""cubicweb-subprocess application packaging information"""

modname = 'subprocess'
distname = 'cubicweb-subprocess'

numversion = (0, 4, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'This cube helps to manage and monitor subprocesses.'
web = 'http://www.cubicweb.org/project/%s' % distname

__depends__ = {'cubicweb': '>= 3.19.1',
               'six': '>= 1.4.0',
               'cubicweb-file': '>= 1.16.0'}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]
