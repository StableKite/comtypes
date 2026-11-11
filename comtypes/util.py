"""Byte-offset ctypes references and structure field access."""

from ctypes import POINTER, Structure, _SimpleCData, byref, cast
from ctypes import Array as _CArrayType
from typing import TYPE_CHECKING, TypeVar, overload

if TYPE_CHECKING:
    from ctypes import _CArgObject, _CData

_T = TypeVar("_T")
_CT = TypeVar("_CT", bound="_CData")


@overload
def byref_at(obj: _CArrayType, offset: int) -> "_CArgObject": ...
@overload
def byref_at(obj: "_CData", offset: int) -> "_CArgObject": ...
def byref_at(obj, offset, _byref=byref):
    """Return a reference to obj plus offset bytes, retaining its owner."""
    return _byref(obj, offset)


@overload
def cast_field(
    struct: Structure, fieldname: str, fieldtype: type["_SimpleCData[_T]"]
) -> _T: ...
@overload
def cast_field(struct: Structure, fieldname: str, fieldtype: type[_CT]) -> _CT: ...
def cast_field(
    struct,
    fieldname,
    fieldtype,
    _POINTER=POINTER,
    _byref_at=byref_at,
):
    """cast_field(struct, fieldname, fieldtype)

    Return the contents of a struct field as it it were of type
    'fieldtype'.
    """
    fieldoffset = getattr(type(struct), fieldname).offset
    return cast(_byref_at(struct, fieldoffset), _POINTER(fieldtype))[0]


__all__ = ["byref_at", "cast_field"]
