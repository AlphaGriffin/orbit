    Copyright (C) 2018 Alpha Griffin
    @%@~LICENSE~@%@

ORBIT Specification
===================

All information concerning ORBIT events are stored on the Bitcoin Cash blockchain as data captured by OP_RETURN.

ORBIT events are identified by OP_RETURN data that begins with the following 4-byte hexadecimal sequence::

    A4 20 19 81

**FIXME: this file is not yet complete.**


Version 0
---------

This is the first version of the specification, currently undergoing mainnet testing.

ORBIT genesis block: **541337**


Considerations
--------------

There are a number of things that should be taken into consideration...

Proof of Ownership
~~~~~~~~~~~~~~~~~~

Token event transactions must be signed with a public key matching the token address (for admin events) or the user address. Since the BCH nodes validate that the transaction signer controls the tx inputs, and the signer's public key is included in the signature, the ORBIT node can simply check that the public key used to sign the transaction inputs maps to the address in question in order to verify it is under the event originator's control.

In the future we might want to include other proof mechanisms in the specification.

Confirmations
~~~~~~~~~~~~~

How many BCH confirmations should be required for an ORBIT node to include an event? Currently, a single confirmation is deemed to be sufficient.

Ambiguity
~~~~~~~~~

Token symbols (and names) are allowed to be duplicated. It is recommended that user interfaces attach a warning to any tokens duplicating the properties of an existing token.

Censorship
~~~~~~~~~~

User interfaces (websites, notably) may want to obscure or completely hide token symbols, names, or images that are deemed illegal or offensive.

