=====================
pyArchOps/helpers
=====================


.. image:: https://badge.fury.io/py/pyarchops-helpers.svg
        :target: https://pypi.python.org/pypi/pyarchops-helpers

.. image:: https://img.shields.io/gitlab/pipeline/gitlab-org/gitlab-ce/master.svg
        :target: https://gitlab.com/pyarchops/helpers/pipelines

.. image:: https://readthedocs.org/projects/pyarchops-helpers/badge/?version=latest
        :target: https://pyarchops-helpers.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/pyarchops/helpers/shield.svg
     :target: https://pyup.io/repos/github/pyarchops/helpers/
          :alt: Updates


helpers


* Free software: MIT license
* Documentation: https://pyarchops-helpers.readthedocs.io.


Features
--------

* helpers

Usage
--------

.. code-block:: python

    import os
    import pyarchops_helpers

    api = Api(
        '127.0.0.1:22',
        connection='smart',
        remote_user='ubuntu',
        private_key_file=os.getenv('HOME') + '/.ssh/id_rsa',
        become=True,
        become_user='root',
        sudo=True,
        ssh_extra_args='-o StrictHostKeyChecking=no'
    )
    result = pyarchops_helpers.apply(api)
    print(result)

Development
-----------

Install requirements:

.. code-block:: console

    $ sudo pacman -S tmux python-virtualenv python-pip libjpeg-turbo gcc make vim git tk tcl

Git clone this repository

.. code-block:: console

    $ git clone https://github.com/pyarchops/helpers.git pyarchops.helpers
    $ cd pyarchops.helpers


2. See the `Makefile`, to get started simply execute:

.. code-block:: console

    $ make up


Credits
-------

* TODO

