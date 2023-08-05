# pylint: disable=W0622
"""cubicweb-processing application packaging information"""

modname = 'processing'
distname = 'cubicweb-processing'

numversion = (0, 9, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'cube that describes simple data processing workflows'
web = 'http://www.cubicweb.org/project/%s' % distname



__depends__ = {'cubicweb': '>= 3.22.0',
               'six': '>= 1.4.0',
               'cubicweb-file': '>= 1.11.0',
               'cubicweb-wireit': '>= 0.3.0'}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]

