=========================
pyk8sver 
=========================

*pyk8sver* returns the latest version of kubernetes

Requirements
============

TBD

Setup
=====

* If you want to run the test cases, do this extra step

.. sourcecode:: bash

    pip install -r requirements-dev.txt

* Install the package:

.. sourcecode:: bash

    python setup.py develop

* (Optional) Run all tests:

.. sourcecode:: bash

    $ paver test_all
    ======================== 112 passed, 2 xfailed in 2.01 seconds
     ___  _   ___ ___ ___ ___
    | _ \/_\ / __/ __| __|   \
    |  _/ _ \\__ \__ \ _|| |) |
    |_|/_/ \_\___/___/___|___/

Example
=======

.. sourcecode:: python

     from pyk8sver import app
     o = app.Kubernetes('your-github-access-token')
     releases = o.fetch_releases()
     print("Latest is {0}".format(releases[0])) # GitRelease(title="v1.13.2")
