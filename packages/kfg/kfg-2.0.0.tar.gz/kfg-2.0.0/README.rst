|Python version| |Build Status|

=========================================
 kfg: A configuration library for Python
=========================================

``kfg`` provides a ``Config`` class which contains your program's configuration
data. It lets you access, manipulate, and validate this data in a
straightforward way. It also provides a means to de/serialize the data.

Basic usage
===========

Setting and retrieving configuration values
-------------------------------------------

Getting and setting configuration values is simple:

.. code-block:: python

   from kfg.config import Config

   # construct a Config
   c = Config()

   # set the ('ui', 'font-color') value to 'blue'
   c['ui', 'font-color'] = 'blue'

   # retreive the value
   font_color = c['ui', 'font-color']

Uniform exceptions
------------------

``kfg`` provides a uniform set of exceptions that are used to signal configuration
problems. This means that your program can catch these exceptions and know that
they only ever indicate configuration problems. For example:

.. code-block:: python

   c = Config()

   # kfg throws ConfigKeyError on missing keys.
   try:
       x = c['foo']
   except ConfigKeyError:
       print('foo not in the config')

Transforms and validation
-------------------------

``kfg`` lets you associate a "transform" with a key. This transform is a 1-arity
callable that will be passed the stored value of the configuration option, and
``kfg`` will pass the return value of the transform to the user when they access
the value. If a transform fails, ``kfg`` will raise a ``ConfigValueError``.

This lets you do two things. First, you can construct arbitrary values from
stored configuration information in a centralized way, i.e. mediated by the
configuration. Second, it let's you validate configuration values. For example:

.. code-block:: python

   c = Config()
   c['processing', 'timeout'] = "10 seconds"
   c.set_transform(('processing', 'timeout'),
                   float)

   c['processing', 'timeout']  # Raises ConfigValueError because ``float``
                               # can't parse "10 seconds"

This system is intentionally low-powered and simple. For example, ``kfg`` allows
you to *set* values which violate the transform. The goal is not to create
completely water-tight configurations, but rather to create systems which are
easy to get right and which warn you when you might be using an invalid value.


Rationale
=========

There's no real rocket science in ``kfg``, and you can get most of its features
just by using dictionaries, lists, tuples, etc. There are a few problems with
using "raw" data structures like that for configuration, though.

First, you'll get standard exceptions like ``KeyError`` and ``IndexError`` when you
try to access missing values. Since these kinds of errors can come from almost
anywhere in a system, it's not easy to differentiate between those that come
from configuration problems and the others. By providing specialized
"configuration" errors, you can catch ``kfg`` exceptions and be confident that
they point to configuration errors.

Second, ``kfg`` lets you centralize the basic configuration
validation/transformations. Configuration values may be used in many places in a
system, so it's often helpful to have a single point of validation for them.


.. |Python version| image:: https://img.shields.io/badge/Python_version-3.4+-blue.svg
   :target: https://www.python.org/
.. |Build Status| image:: https://travis-ci.org/abingham/kfg.png?branch=master
   :target: https://travis-ci.org/abingham/kfg
