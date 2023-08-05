Features
========

* BER/CER/DER decoding, DER encoding
* Basic ASN.1 data types (X.208): BOOLEAN, INTEGER, BIT STRING, OCTET
  STRING, NULL, OBJECT IDENTIFIER, ENUMERATED, all strings, UTCTime,
  GeneralizedTime, CHOICE, ANY, SEQUENCE (OF), SET (OF)
* Size :ref:`constraints <bounds>` checking
* Working with sequences as high level data objects with ability to
  (un)marshall them
* Python 2.7/3.5/3.6 compatibility
* Aimed to be complaint with `X.690-201508 <https://www.itu.int/rec/T-REC-X.690-201508-I/en>`__

Why yet another library? `pyasn1 <http://snmplabs.com/pyasn1/>`__
had all of this a long time ago. PyDERASN resembles it in many ways. In
practice it should be relatively easy to convert ``pyasn1``'s code to
``pyderasn``'s one. But additionally it offers:

* Small, simple and trying to be reviewable code. Just a single file
* Automatic decoding of :ref:`DEFINED BY <definedby>` fields
* Ability to know :ref:`exact decoded <decoding>` objects offsets and
  lengths inside the binary
* :ref:`Pretty printer <pprinting>` and command-line decoder, that could
  conveniently replace utilities like either ``dumpasn1`` or
  ``openssl asn1parse``
* Some kind of strong typing: SEQUENCEs require the exact **type** of
  settable values, even when they are inherited
* However they do not require tags matching: IMPLICIT/EXPLICIT tags will
  be set automatically in the given sequence
* Descriptive errors, like ``pyderasn.DecodeError: UTCTime
  (tbsCertificate:validity:notAfter:utcTime) (at 328) invalid UTCTime format``
* ``__slots__`` friendliness
* Could be significantly faster. For example parsing of CACert.org's CRL
  under Python 3.5.2:

    :``python -m pyderasn revoke.crl``:
     ~2 min (``pyderasn == 1.0``)
    :``python -m pyderasn --schema path.to.CertificateList revoke.crl``:
     ~38 sec (``pyderasn == 1.0``)
    :``pyasn1.decode(asn1Spec=pyasn1.CertificateList())``:
     ~22 min (``pyasn1 == 0.2.3``)

There are drawbacks:

* No old Python versions support
* Strings are not validated in any way, except just trying to be decoded
  in ``ascii``, ``iso-8859-1``, ``utf-8/16/32`` correspondingly
* No REAL, RELATIVE OID, EXTERNAL, INSTANCE OF, EMBEDDED PDV, CHARACTER STRING
