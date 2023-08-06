===============================
resize
===============================

.. image:: https://badge.fury.io/py/resize.png
    :target: http://badge.fury.io/py/resizer

.. image:: https://travis-ci.org/bdabrowski/resize.png?branch=master
        :target: https://travis-ci.org/bdabrowski/resizer

.. image:: https://pypip.in/d/resize/badge.png
        :target: https://crate.io/packages/resizer?version=latest


Simple command line utility for re-sizing images in a batch operation.

Usage:
  resize.py <path> [--height=<px>] [--width=<px>]
  resize.py -h | --help
  resize.py --version

Options:
  -h --help           Show this screen.
  -v --version        Show version.
  -O --output-dir     Full path to directory with photos (./processed is default)
  -H --height=<px>    Set resulting height in pixels as number. [Default 1024]
  -W --width=<px>     Set resulting width in pixels as number. [Default 768]

Example:
    resize.py . --height=1024 --width=768

Results in creating subdirectory "processed" with all processed images inside.

Requirements
------------

- Python >= 2.7 or >= 3.7

License
-------

MIT licensed. See the bundled `LICENSE <https://github.com/bdabrowski/resize/blob/master/LICENSE>`_ file for more details.
