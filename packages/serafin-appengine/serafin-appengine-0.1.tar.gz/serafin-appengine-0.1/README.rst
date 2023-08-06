
#################
serafin-appengine
#################

**serafin-appengine** is a small python library that provides Google Datastore
models integration for *serafin*.

.. note::
The project follows the semantic versioning scheme: Until 1.0 the minor

        * The *patch* versions only include bugfixes and changes that do not
          modify the existing interface. You can safely update a patch version
          without worrying it will break your code.
        * The *minor* versions will contain changes to the interface. With a
          single version update your code will most likely work or might require
          small adjustments. The more minor versions you update at once the
          bigger the chance that something will brake.
        * The *major* versions are reserved for significant refactorings and
          architecture changes. This should not happen very often so the major
          version should not change much.

.. note::
    The CircleCI builds can be found
    `here <https://circleci.com/gh/novopl/serafin-appengine>`_

.. readme_inclusion_marker

Installation
============

.. code-block:: shell

    $ pip install serafin-appengine


Contributing
============

Setting up development repo
---------------------------

.. code-block:: shell

    $ git clone git@github.com:novopl/serafin-appengine.git
    $ cd serafin
    $ virtualenv env
    $ source ./env/bin/activate
    $ pip install -r ops/devrequirements.txt
    $ python setup.py develop
    $ peltak git add-hoooks


Running tests
.............

**Config**: The types of tests are defined in ``pelconf.py`` and the
pytest configuration is defined in ``ops/tools/pytest.ini``.

.. code-block:: shell

    $ peltak test

Linting
.......

**Config**: The list of locations to lint is defined in ``pelconf.py`` and the
linters configuration is defined in ``ops/tools/{pylint,pep8}.ini``.

.. code-block:: shell

    $ peltak lint

Generating docs
...............

**Config**: The list of documented files and general configuration is in
``pelconf.py`` and the Sphinx configuration is defined in ``docs/conf.py``.

.. code-block:: shell

    $ peltak docs
