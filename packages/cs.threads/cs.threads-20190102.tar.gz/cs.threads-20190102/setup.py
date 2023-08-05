#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.threads',
  description = 'threading and communication/synchronisation conveniences',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190102',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.debug', 'cs.excutils', 'cs.logutils', 'cs.obj', 'cs.py.func', 'cs.py3', 'cs.queues', 'cs.seq'],
  keywords = ['python2', 'python3'],
  long_description = "Thread related convenience classes and functions.\n\n## Class `AdjustableSemaphore`\n\nA semaphore whose value may be tuned after instantiation.\n\n## Function `bg(func, daemon=None, name=None)`\n\nDispatch the callable `func` in its own Thread; return the Thread.\n\nParameters:\n`daemon`: optional argument specifying the .daemon attribute.\n`name`: optional argument specifying the Thread name.\n\n## Class `LockableMixin`\n\nTrite mixin to control access to an object via its ._lock attribute.\nExposes the ._lock as the property .lock.\nPresents a context manager interface for obtaining an object's lock.\n\n## Function `locked(func)`\n\nA decorator for monitor functions that must run within a lock.\nRelies upon a ._lock attribute for locking.\n\n## Function `locked_property(func, lock_name='_lock', prop_name=None, unset_object=None)`\n\nA thread safe property whose value is cached.\nThe lock is taken if the value needs to computed.\n\n## Function `via(cmanager, func, *a, **kw)`\n\nReturn a callable that calls the supplied `func` inside a\nwith statement using the context manager `cmanager`.\nThis intended use case is aimed at deferred function calls.\n\n## Class `WorkerThreadPool`\n\nMRO: `cs.resources.MultiOpenMixin`, `cs.obj.O`  \nA pool of worker threads to run functions.\n\n## Class `WTPoolEntry`\n\nMRO: `builtins.tuple`  \nWTPoolEntry(thread, queue)",
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.threads'],
)
