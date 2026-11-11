This 1.4.17+stablekite.2 review backports upstream comtypes PR #960,
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

The second review uses the standard ctypes.byref(obj, offset) API instead of
reading and changing private PyCArgObject storage. This preserves byte offsets
and owner lifetime independently of CPython's GIL and private object layout.
PumpEvents retains one C callback through registration and unregistration, and
unregisters it before closing the event handle. The frozen-DLL cache test uses
the actual DLL filename, including its free-threaded suffix, rather than assuming
the executable and DLL have the same basename. The original GC assertion stays.

Normal CoWaitForMultipleHandles timeout results are handled as HRESULT values,
avoiding ctypes' synthetic exception traceback on this expected path. Other
failing HRESULTs still raise OSError and a signaled wait still interrupts.
Borrowed COM pointer views do not release the owner's reference. Temporary
owned pointers retain balanced AddRef/Release in VARIANT and SAFEARRAY access.
Actual native COM reference counts, owner lifetime and both containers have
dedicated regression tests. No original GC or reference-count assertion is
weakened. Codecov uses its documented GitHub OIDC authentication; its upload
failure remains a failed gate and original tests/matrices stay in place.
