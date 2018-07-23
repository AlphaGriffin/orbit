============================================
ORBIT - Op_Return Bitcoin Implemented Tokens
============================================

**A token standard specification and API for Bitcoin Cash**

The official website for ORBIT is http://orbit.alphagriffin.com.

.. contents:: Table of Contents
.. toctree::
   API Documentation <api/modules>


Introduction
------------

ORBIT is a specification for simple, fungible tokens implemented by utilizing OP_RETURN for the storage of token events on the Bitcoin Cash blockchain. No changes to the Bitcoin Cash protocol or nodes are required. However, wallets may wish to incorporate this token standard in order to allow the user to easily take account of and interact with tokens that adhere to this ORBIT standard.

ORBIT is open source and licensed under the MIT license. See the `LICENSE` file for more details.


Specification Overview
----------------------

This repository (https://github.com/AlphaGriffin/orbit) defines the official and complete specification for ORBIT. 

*The current specification version is **0** (beta testing). Version 0 is reserved and should be used for all testing.*

Only a basic overview of the specification is provided in this section. You will find the full text specifying the ORBIT standard in the `SPECIFICATION.rst` file.

**FIXME: Finish this section**


API
---

This repository also provides a simple Python 3 API for transacting with and retrieving information about any ORBIT-compliant token on Bitcoin Cash.


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

There's not much to do for a simple Python project but your build may want to do more. In any case you can call ``make python`` if you need to (in orbit this target simply delegates to ``./setup.py build``).

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

The **orbit** module does nothing useful and is for example purposes only, but you can import it to verify correct installation.

If you have already installed the project to the system then it's as simple as::
    
    import ag.orbit

If you have not installed the project system-wide or you have some changes to try, you must add the project folder to Python's search path first::

    import sys, os
    sys.path.insert(0, os.path.abspath('/path/to/orbit'))
    import ag.orbit

