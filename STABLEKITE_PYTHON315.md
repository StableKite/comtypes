This 1.4.17+stablekite.1 review backports upstream comtypes PR #960,
commit 644ee92a7d5891621d97aed300356c629557afd4, with its author and
origin retained in the Git history.

Friendly enumerations containing negative values use IntEnum so their integer
values agree with the real type library on Python 3.15. Nonnegative enumerations
retain IntFlag and its bitwise operations. The raw COM wrapper still declares
enumeration storage as ctypes.c_int; no COM ABI layout or vtable changes are made.
This intentionally follows upstream's enum-class choice on older Python too.

The existing enum assertions remain, the obsolete prerelease skip is removed,
and upstream's actual type-library base-class test is included. The blanket
Python 3.15 warning is removed as part of this functional upstream correction.
Existing generated modules must be regenerated to use the corrected friendly
classes; fresh installations have their own generated-module cache.

No consumer source, checking rules, SDK, COM registration or warning filter is
changed by this source patch. Native tests and the full original workflow are
qualified separately; this document does not claim those pending gates passed.
