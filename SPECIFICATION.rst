ORBIT Specification
===================

All information concerning ORBIT events is stored on the Bitcoin Cash blockchain as data captured by OP_RETURN.

.. contents:: Specification Contents
   :local:



Goals
-----

- **Simple** implementation that any average developer can understand.
- **No changes required** to the Bitcoin protocol or Bitcoin Cash nodes.
- **Low fee** transactions accomplished by keeping the payload data small.
- Supporting token **crowd sales** and **free faucets** with no additional fees or conversions. Only the very low cost of a Bitcoin Cash transaction fee is required to create a new token. All token events and crowd-sale payments are made directly with Bitcoin Cash satoshis.
- **Easy validation** so that any user can independently confirm token balances by running their own lightweight ORBIT node.
- **Open source** with a permissive license so anybody is free to use and modify the code as they wish.



General Form for OP_RETURN Data
-------------------------------

ORBIT events are identified by the presence of OP_RETURN data of the following general form::

    <PREAMBLE> <VERSION> <CONTINUES> <ADDRESS> <OPERATION>

Multibyte data is always stored as big endian (most-significant bytes first).


PREAMBLE
^^^^^^^^

The following 4-byte hex sequence identifies the beginning of an ORBIT event::

    A4 20 19 81

VERSION
^^^^^^^

Following the PREAMBLE is a single byte that indicates the specification major version number. The current version is::

    00

CONTINUES
^^^^^^^^^

A single byte indicating the number of OP_RETURN messages that follow which should be appended to this data to form a complete operation. This exists only for possible future use, since the BCH nodes currently allow only a single OP_RETURN output per transaction. Thus, today this should always contain a zero value::

    00

ADDRESS
^^^^^^^

Address identifies the token address. It consists of a single byte indicating the address version, followed by a single byte indicating the size of the address payload, followed by a variable number of bytes for the address itself::

    FIXME

OPERATION
^^^^^^^^^

The operation indicates the type of ORBIT event. It begins with a single byte which identifies the type of operation, followed by optional payload that is defined by and specific to the operation indicated::

    <OPCODE> [<PAYLOAD>]



Version 0 Details
-----------------

This is the *test* version of the specification, currently undergoing mainnet testing.

ORBIT launch block: **542161**

OP_CREATE
^^^^^^^^^

Create a new token definition.

* Available to: **admin only**

OP_TRANSFER
^^^^^^^^^^^

Transfer tokens from one address to another.

* Available to: **admin or user**

OP_ADVERTISE
^^^^^^^^^^^^

Advertise a crowd-sale or free faucet.

* Available to: **admin only**

OP_ADVERTISE_CANCEL
^^^^^^^^^^^^^^^^^^^

Cancel an advertisement created with ``OP_ADVERTISE``. Cancellation is only allowed if nobody has yet registered with ``OP_REGISTER``.

* Available to: **admin only**

OP_REGISTER
^^^^^^^^^^^

Receive tokens from a crowd-sale or free faucet.

* Available to: **user only**

OP_UNREGISTER
^^^^^^^^^^^^^

End the registration interest created with ``OP_REGISTER``.

* Available to: **user only**



Examples
--------

**FIXME: this file is not yet complete.**



Considerations
--------------

There are a number of things that should be taken into consideration...

Proof of Ownership
^^^^^^^^^^^^^^^^^^

Token event transactions must be signed with a public key matching the token address (for admin events) or the user address. Since the BCH nodes validate that the transaction signer controls the tx inputs, and the signer's public key is included in the signature, the ORBIT node can simply check that the public key used to sign the transaction inputs maps to the address in question in order to verify it is under the event originator's control.

In the future we might want to include other proof mechanisms in the specification.

Confirmations
^^^^^^^^^^^^^

How many BCH confirmations should be required for an ORBIT node to include an event? Currently, a single confirmation is deemed to be sufficient.

Ambiguity
^^^^^^^^^

Token symbols (and names) are allowed to be duplicated. It is recommended that user interfaces attach a warning to any tokens duplicating the properties of an existing token.

Censorship
^^^^^^^^^^

User interfaces (websites, notably) may want to obscure or completely hide token symbols, names, or images that are deemed illegal or offensive. It is not recommended to enforce censorship at the node level.

Payment Refunds
^^^^^^^^^^^^^^^

BCH payments may be sent to a contract for a crowdsale, and ORBIT nodes are able to validate the payment and transfer tokens to the user based on the advertised exchange rate. However, if the user makes a payment that is too small to meet the minimum, too large that it exceeds the advertised per-user limit, or a full exchange cannot be completed because available tokens have been exhausted or the sale has ended, there is no way for ORBIT to refund the payment. This is because the token addresses (where payments are sent) are not under control of the ORBIT ecosystem.

Supporting Multiple Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As this specification evolves, a new major version may be proposed with new features and changes that are not backwards-compatible. Rather than replacing the existing version(s) and the infrastructure that was built up, it might be preferable to push the new version as a complementary standard that coexists with the previous release(s). In such case, it is recommended that we include the major version number as part of the standard name and treat them as separate implementations, e.g. ORBIT-1 tokens and ORBIT-2 tokens.

Supply Locked for Crowd-Sale/Faucet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When ``OP_ADVERTISE`` is used, we currently lock away the units made available for the crowd-sale or faucet so that they are guaranteed to be available solely for this purpose and may not be manually transferred away or destroyed. This may be reconsidered in a future version.

Cross-Node Consistency
^^^^^^^^^^^^^^^^^^^^^^

Although it is recommended that users run their own validating ORBIT node in order to guarantee they're seeing an accurate representation of tokens and balances, it's understood that this isn't always possible. So with this in mind, we want a mechanism where ORBIT nodes can easily communicate with each other to make sure they all agree on the state of tokens and balances at any given block. This could be accomplished by computing a hash on the entire set (retrieved in a deterministic and ordered fashion) and comparing it with neighboring nodes.

BCH vs. ORBIT Validation
^^^^^^^^^^^^^^^^^^^^^^^^

Just because a transaction is accepted into and confirmed by the BCH network does not mean it is guaranteed to be accepted by ORBIT nodes. Nodes should provide a mechanism for the front-ends to check the validity of a transaction before broadcasting. However, even a transaction that was checked to be valid by ORBIT, broadcasted, and confirmed by BCH all during the same block does not guarantee success. This is because other transactions included in that same block with a higher priority may affect the validity of the transaction.

Address Reuse
^^^^^^^^^^^^^

We currently reuse addresses for tokens and users (that is, a single address receives multiple transactions). This is frowned upon by the Bitcoin community. See https://en.bitcoin.it/wiki/Address_reuse for more information.

Bad Assumptions
^^^^^^^^^^^^^^^

The primary developer is by no means a Bitcoin expert. There could be any number of assumptions made about the way Bitcoins are processed that are potentially unsafe. Getting more eyes on the specifiction and code would go a long way towards removing bad assumptions!

Flask Not for Production
^^^^^^^^^^^^^^^^^^^^^^^^

We are currently using the Flask server to handle web API requests. However, Flask is intended for development use only, not production use.



Open Source
-----------

This specification and all included ORBIT source files are free and open source using the MIT license.

.. include:: LICENSE

