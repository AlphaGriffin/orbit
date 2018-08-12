############################################
ORBIT - Op_Return Bitcoin-Implemented Tokens
############################################

.. image:: https://badges.gitter.im/AlphaGriffin/orbit.svg
   :alt: Join the chat at https://gitter.im/AlphaGriffin/orbit
   :target: https://gitter.im/AlphaGriffin/orbit?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

**Token standard specification and API for Bitcoin Cash**

The official website for ORBIT is http://orbit.cash.

.. contents:: Table of Contents
   :depth: 2
   :local:



************
Introduction
************

ORBIT is a specification for simple, fungible tokens implemented by utilizing OP_RETURN for the storage of token events on the Bitcoin Cash blockchain. No changes to the Bitcoin Cash protocol or nodes are required. However, wallets may wish to incorporate this token standard in order to allow the user to easily take account of and interact with tokens that adhere to this ORBIT standard.

ORBIT is open source and licensed under the MIT license. See the `LICENSE <LICENSE>`_ file for more details.


The ORBIT Ecosystem
===================

The following projects, when used in conjunction with the ORBIT API, complete a full ecosystem for tokens on Bitcoin Cash using ORBIT:

- ORBIT Node: https://github.com/AlphaGriffin/orbit-node
- ORBIT Command-Line Interface: https://github.com/AlphaGriffin/orbit-cli
- ORBIT Qt Wallet: https://github.com/AlphaGriffin/orbit-gui
- ORBIT Web: https://github.com/AlphaGriffin/orbit-web



********
Features
********

- All operations possible with very low fees (usually under 1,000 satoshis)
- Anybody can easily create and manage a new token
- Easily start a crowd-sale or faucet



*************
Specification
*************

This repository (https://github.com/AlphaGriffin/orbit) defines the official and complete specification for ORBIT. 

*The current specification version is: 0 (beta testing). Version 0 is reserved and should be used for all testing.*

You will find the full text specifying the ORBIT standard in the `SPECIFICATION <SPECIFICATION.rst>`_ file (included here in generated documentation).

.. include:: SPECIFICATION.rst



************
Contributing
************

Your help is appreciated! Alpha Griffin is a small team focused on developing new technology projects. If you have questions or comments or would like to contribute to the ORBIT specification or ecosystem in any way, please feel free to contact us. You may submit issues or pull requests directly on GitHub or communicate with the team members at the following locations:

- https://gitter.im/AlphaGriffin
- https://alphagriffintrade.slack.com

Have a suggestion or request? Let us know!


To-Do List
==========

There are a number of tasks already identified on the `To-Do list <TODO>`_ that could use your help (included here in generated documentation).

.. include:: TODO
   :literal:



**************
Python Library
**************

This repository also provides a simple Python 3 API for transacting with and retrieving information about any ORBIT-compliant token on Bitcoin Cash.

.. toctree::
   API Documentation <api/modules>


Dependencies
============

- Python 3
- rfc3986 (``pip install rfc3986``)
- BitCash >= 0.5.2.4: https://github.com/sporestack/bitcash (``pip install bitcash\>=0.5.2.4``)
- *For building documentation (optional):* Sphinx and sphinx_rtd_theme (``pip install sphinx sphinx_rtd_theme``)


Quick Start
===========

**FIXME**


Build Overview
==============

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
==========

To install this project to the local system::

    make install

Note that you may need superuser permissions to perform the above step.


Using
=====

The **orbit** module is an API that you can import and use in any Python 3 project.

If you have already installed the project to the system then it's as simple as::
    
    import ag.orbit

If you have not installed the project system-wide or you have some changes to try, you must add the project folder to Python's search path first::

    import sys, os
    sys.path.insert(0, os.path.abspath('/path/to/orbit'))
    import ag.orbit



*******
History
*******

All changes are tracked in the `CHANGELOG <CHANGELOG>`_ file.

.. include:: CHANGELOG
   :literal:

----

*"Orbit the moon"*

