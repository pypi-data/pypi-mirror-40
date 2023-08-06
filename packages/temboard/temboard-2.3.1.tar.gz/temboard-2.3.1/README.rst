| |temBoard|

Monitor, optimize and configure multiple PostgreSQL instances.

| |Python| |RTD| |CircleCI| |Codecov| |PyPI|

| |Demo|


=========
 Install
=========

temBoard is composed of 2 basic elements:

- A lightweight **agent** that you need to install on every PostgreSQL server
  you want to manage. See `dalibo/temboard-agent`_ for the agent project.
- A central **web app** (this project) to control the agents and collect metrics.


temBoard needs a dedicated database called *repository* to store configuration,
metrics and other data.

::

    pip install temboard
    sudo -u postgres bash /usr/local/share/temboard/create_repository.sh
    temboard -c /usr/local/share/temboard/quickstart/temboard.conf

Now install `dalibo/temboard-agent`_ along the PostgreSQL cluster you want to
administer and register it in the UI. Further details on
`temboard.readthedocs.io <http://temboard.readthedocs.io/en/latest/>`_.


===================
 Docker Quickstart
===================

We provide a complete *testing* environment based on Docker ! Please read our
`QUICKSTART <https://github.com/dalibo/temboard/blob/master/QUICKSTART.md>`_
guide for more details.


============
 Contribute
============

temBoard is an open project. Any contribution to improve it is welcome.

Want to contribute? Please first read our guide on `contributing
<https://github.com/dalibo/temboard/blob/master/CONTRIBUTING.md>`_ if you're
interested in getting involved.


=========
 License
=========

temBoard is available under the `PostgreSQL License
<https://github.com/dalibo/temboard/blob/master/LICENSE>`_.


.. |CircleCI| image:: https://circleci.com/gh/dalibo/temboard.svg?style=shield
   :target: https://circleci.com/gh/dalibo/temboard
   :alt: CircleCI

.. |CodeCov| image:: https://codecov.io/gh/dalibo/temboard/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/dalibo/temboard
   :alt: Code coverage

.. |Demo| image:: https://github.com/dalibo/temboard/raw/master/doc/sc/alerting_dashboard.png
   :target: https://github.com/dalibo/temboard/raw/master/doc/sc/alerting_dashboard.png
   :alt: Screenshot temBoard

.. |PyPI| image:: https://img.shields.io/pypi/v/temboard.svg
   :target: https://pypi.python.org/pypi/temboard
   :alt: Version on PyPI

.. |Python| image:: https://img.shields.io/pypi/pyversions/temboard.svg
   :target: https://www.python.org/
   :alt: Versions of python supported

.. |RTD| image:: https://readthedocs.org/projects/temboard/badge/?version=latest
   :target: http://temboard.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation

.. |temBoard| image:: https://github.com/dalibo/temboard/raw/master/doc/temboard.png
   :target: http://temboard.io/
   :alt: temBoard logo: a woodpecker

.. _dalibo/temboard-agent: https://github.com/dalibo/temboard-agent
