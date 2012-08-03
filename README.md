
CouchDB Auth/Auth for Pyramid
=============================

[CouchDB][1] authorization/authentication plugins for [Pyramid][2].


Installation from Source
------------------------

There are currently no official releases of pyramid_couchauth. As such you will need to build and install the code by hand.

First, retrieve the source code:

    git clone --depth 1 git://github.com/BlueDragonX/pyramid_couchauth.git

Then enter the project directory and build the egg:

    cd pyramid_couchauth
    python setup.py bdist_egg

Lastly install the egg:

    easy_install dist/pyramid_couchauth*.egg


Usage Example
-------------

A working example is available on [github][3].


Authors
-------

The pyramid_couchauth project is the product of work by the following people:

- Ryan Bourgeois <bluedragonx@gmail.com>


License
-------

The pyramid_couchauth project is licensed under the BSD-derived license and is
copyright (c) 2012 Ryan Bourgeois. A copy of the license is included in the
LICENSE file. If it is missing a copy can be found on the [project page][4].


[1]: http://couchdb.apache.org/ CouchDB
[2]: http://pylonsproject.org/ Pyramid
[3]: https://github.com/BlueDragonX/pyramid_couchauth_example/ pyramid_couchauth_example
[4]: https://github.com/BlueDragonX/pyramid_couchauth/blob/master/LICENSE License

