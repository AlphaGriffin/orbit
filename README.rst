====================================
Alpha Griffin Python Starter Project
====================================

Starting point for a Python project in the Alpha Griffin namespace.

Use http://git.alphagriffin.com/DummyScript/fauxpython instead if you're not packaging for Alpha Griffin.

.. contents:: Table of Contents
.. toctree::
   API Documentation <api/modules>


Starting a Project
------------------

You can use this repository as a starting point for any Alpha Griffin Python project. Here's an example of one way to accomplish this with GitHub:

1. Start a new repository on GitHub but **do not initialize** as you will be pushing an existing repository (a clone of pyproject). For this example we'll name it *my_new_thing*.
2. ``git clone http://git.alphagriffin.com/AlphaGriffin/pyproject my_new_thing``
3. ``cd my_new_thing``
4. ``git remote remove origin``
5. ``git remote add origin http://git.alphagriffin.com/AlphaGriffin/my_new_thing``
6. ``git push -u origin master``

Now your clone of pyproject lives at the new GitHub address and pushes will go there by default.

**Recommended**

With this extra step you can easily pull and merge again in the future from this master *pyproject* repository:

7. ``git remote add pyproject http://git.alphagriffin.com/AlphaGriffin/pyproject``

Using ``git pull pyproject master`` you can pull and merge the latest from *pyproject* at any time.


First Commit
------------

There's a few things you'll want to do for first commit:

1. Rename the default project source folder: ``git mv ag/pyproject ag/my_new_thing``. It's important you have a similar ``__version__.py`` file in your source folder.
2. Update variables in ``setup.py``, most importantly NAME must match the name of your new ``ag/my_new_thing`` source folder
3. Remove the pyproject API rst docs from ``api/`` folder. You can use ``make apidoc_clean apidoc`` to have new ones automatically generated once you have some code to document.


Build Overview
--------------

Both a Makefile and setup.py are provided and used. The setup.py uses Python's standard setuptools package and you can call this script directly to do the basic Python tasks such as creating a wheel, etc.

The most common project build tasks are all provided in the Makefile. To see the full list of project targets::

    make help

Sphinx is used to generate html documentation and man pages. All documentation (html as well as man pages) may be regenerated at any time with::

    make docs

Every so often, when new source class files are created or moved, you will want to regenerate the API documentation templates. These templates may be modified by hand so this task does not overwrite existing files; you'll need to remove any existing files from ``api/`` that you want recreated. Then generate the API templates and re-build all documentation as follows::

    make apidoc
    make docs

There's not much to do for a simple Python project but your build may want to do more. In any case you can call ``make python`` if you need to (in pyproject this target simply delegates to ``./setup.py build``).

Build all the common tasks (including documentation) as follows::

    make all

To clean up all the common generated files from your project folder::

    make clean


Installing
----------

To install this project to the local system::

    make install

Note that you may need superuser permissions to perform the above step.


Using
-----

The **pyproject** module does nothing useful and is for example purposes only, but you can import it to verify correct installation.

If you have already installed the project to the system then it's as simple as::
    
    import ag.pyproject

If you have not installed the project system-wide or you have some changes to try, you must add the project folder to Python's search path first::

    import sys, os
    sys.path.insert(0, os.path.abspath('/path/to/pyproject'))
    import ag.pyproject

