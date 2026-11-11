import ctypes
import gc
import unittest

from comtypes import COMObject, IUnknown
from comtypes.automation import VARIANT, _midlSAFEARRAY


class Example(COMObject):
    _com_interfaces_ = [IUnknown]


class BorrowedCOMPointerTest(unittest.TestCase):
    def test_borrowed_contents_does_not_release_owner_reference(self):
        owner = Example()
        pointer = owner.QueryInterface(IUnknown)
        outer = ctypes.cast(ctypes.byref(pointer), ctypes.POINTER(type(pointer)))
        alias = outer.contents
        self.assertIs(alias._b_base_, outer)
        self.assertEqual(owner._refcnt.value, 1)
        del alias
        gc.collect()
        self.assertEqual(owner._refcnt.value, 1)
        del outer, pointer
        gc.collect()
        self.assertEqual(owner._refcnt.value, 0)

    def test_borrowed_contents_keeps_owner_alive(self):
        owner = Example()
        pointer = owner.QueryInterface(IUnknown)
        outer = ctypes.pointer(pointer)
        alias = outer.contents
        del outer, pointer
        gc.collect()
        self.assertEqual(owner._refcnt.value, 1)
        independent = alias.QueryInterface(IUnknown)
        self.assertEqual(owner._refcnt.value, 2)
        del independent
        gc.collect()
        self.assertEqual(owner._refcnt.value, 1)
        del alias
        gc.collect()
        self.assertEqual(owner._refcnt.value, 0)

    def test_variant_and_returned_pointer_keep_independent_references(self):
        owner = Example()
        pointer = owner.QueryInterface(IUnknown)
        variant = VARIANT(pointer)
        self.assertEqual(owner._refcnt.value, 2)
        returned = variant.value
        self.assertEqual(owner._refcnt.value, 3)
        del returned
        gc.collect()
        self.assertEqual(owner._refcnt.value, 2)
        variant.value = None
        self.assertEqual(owner._refcnt.value, 1)
        del pointer
        gc.collect()
        self.assertEqual(owner._refcnt.value, 0)

    def test_safearray_and_unpacked_pointers_have_balanced_references(self):
        owner = Example()
        pointer = owner.QueryInterface(IUnknown)
        array = _midlSAFEARRAY(ctypes.POINTER(IUnknown)).from_param([pointer, pointer])
        gc.collect()
        self.assertEqual(owner._refcnt.value, 3)
        returned = array[0]
        gc.collect()
        self.assertEqual(owner._refcnt.value, 5)
        del returned
        gc.collect()
        self.assertEqual(owner._refcnt.value, 3)
        del array
        gc.collect()
        self.assertEqual(owner._refcnt.value, 1)
        del pointer
        gc.collect()
        self.assertEqual(owner._refcnt.value, 0)
