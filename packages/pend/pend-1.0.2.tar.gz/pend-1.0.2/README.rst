pend
--------------------------------

.. image:: https://badge.fury.io/py/pend.svg
    :target: https://badge.fury.io/py/pend

This is wrapper of pendulum.

:code:`Pendulum` is too long and a hassle to type. But :code:`pend` is easy. That's just it.

* `pendulum repository`_
* `pendulum site`_

.. _pendulum repository: https://github.com/sdispater/pendulum
.. _pendulum site: https://pendulum.eustace.io/

Install
=========

.. code::

    pip install pend

Use
======

.. code-block:: python

    >>> import pend

    >>> now_in_paris = pend.now('Europe/Paris')
    >>> now_in_paris
    '2016-07-04T00:49:58.502116+02:00'

    # Seamless timezone switching
    >>> now_in_paris.in_timezone('UTC')
    '2016-07-03T22:49:58.502116+00:00'

    >>> tomorrow = pend.now().add(days=1)
    >>> last_week = pend.now().subtract(weeks=1)

    >>> past = pend.now().subtract(minutes=2)
    >>> past.diff_for_humans()
    >>> '2 minutes ago'

    >>> delta = past - last_week
    >>> delta.hours
    23
    >>> delta.in_words(locale='en')
    '6 days 23 hours 58 minutes'

    # Proper handling of datetime normalization
    >>> pend.datetime(2013, 3, 31, 2, 30, tz='Europe/Paris')
    '2013-03-31T03:30:00+02:00' # 2:30 does not exist (Skipped time)

    # Proper handling of dst transitions
    >>> just_before = pend.datetime(2013, 3, 31, 1, 59, 59, 999999, tz='Europe/Paris')
    '2013-03-31T01:59:59.999999+01:00'
    >>> just_before.add(microseconds=1)
    '2013-03-31T03:00:00+02:00'

