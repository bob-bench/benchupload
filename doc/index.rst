bob-bench.org metric upload
===========================

Contents:

.. toctree::
   :maxdepth: 2

About
=====

benchupload_ is a small Python utility that can be used to
find and upload xUnit files to bob-bench.org_ from a
continous integration build. In the future more than xUnit
will be supported. It is known to work with Python 2.7,
Python 3.3 or later.

.. _benchupload: https://github.com/bob-bench/benchupload
.. _bob-bench.org: https://www.bob-bench.org

Features
--------

The xUnit file will be analyzed and stored for future
analysis. A badge_ can be generated that will show the amount
of tests (or failures) on a project page. On the bob-bench.org_
website one can browse results and look at the output.

.. _badge: https://api.bob-bench.org/v1/badge/8?branch=master

Options
-------

The utility has a limited amount of arguments. These include
the URL of the upload server and the base directory to search
for xUnit files.

-h, --help	Show this help message and exit
--dir=DIR	Start in this directory to search for xUnit files
--url=URL	Uplpad URL

Supported CIs
=============

Currently the circleci_ and travis-ci_ service are supported.
In the future we will add detection for more services. Please
inform us about your demand.

.. _circleci: https://circleci.com
.. _travis-ci: https://travis-ci.org


Circleci
--------

Circleci is continous integration platform with good
docker integration. One needs to install the benchupload
utility and then upload the result. The circle.yml file
needs to be changed to include the following:

.. code-block:: yaml

  dependencies:
    post:
      - pip install benchupload
  test:
    post:
      - python -mbenchupload --dir=$CIRCLE_TEST_REPORTS



Travis-CI
---------

Travis-CI is the first supported system and used during
the development of the bob-bench.org_ service. One needs to
use pip install to install the benchupload utility and then
upload the result. The .travis.yml file needs to be changed
to include the following:

.. code-block:: yaml

  install:
   - pip install --user benchupload
  after_success:
   - python -mbenchupload
  after_failure:
   - python -mbenchupload


Smalltalk CI example
--------------------

If smalltalk-ci is used benchupload should search different
directories for the xUnit files. This can be done by using
the --dir= option. The .travis.yml file needs to be modified
to look like:

.. code-block:: yaml

  after_success:
   - python -mbenchupload --dir=$SMALLTALK_CI_BUILD
  after_failure:
   - python -mbenchupload --dir=$SMALLTALK_CI_BUILD

Project example
---------------

The `moiji-mobile SMSC`_ is hosted on github, using travis-ci
for CI and bob-bench to track the test execution.


.. _moiji-mobile SMSC: https://github.com/moiji-mobile/smsc

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

