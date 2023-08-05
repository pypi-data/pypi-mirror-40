Weka - Python wrapper for Weka Graphics
==========================================

Overview
--------

Provides a convenient wrapper for calling Weka from Python to generate a graph with the data from an arff file.

Installation
------------

First install the Weka and LibSVM Java libraries. On Debian/Ubuntu this is simply:

    sudo apt-get install weka libsvm-java

Then install the Python package with pip:

    sudo pip install QtWekaWrapper

You can find the module on the [PyPi](https://pypi.org/project/QtWekaWrapper/).

Usage
-----

Create a Python 3 environment with the 'virtualenv' module and after activate it. Install the module with `pip install QtWekaWrapper` command and you can instantiate the qt window where the arff file will be loaded:

    from QtWekaWrapper import qtwekawrapper
    window = qtwekawrapper.run_qt_window()

Development
-----------

Tests require the Python development headers to be installed, which you can install on Ubuntu with:

    sudo apt-get install python-dev python3-dev python3.4-dev

To run unittests across multiple Python versions, install:

    sudo apt-get install python3.4-minimal python3.4-dev python3.5-minimal python3.5-dev

To run all [tests](http://tox.readthedocs.org/en/latest/):

    export TESTNAME=; tox

