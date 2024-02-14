from __future__ import annotations

from inspect import getmembers
from typing import Generic, TypeVar, get_args

_Key = TypeVar("_Key", bound=tuple[str, ...])


class _Leaf(Generic[_Key]):
    def __init__(self, name: str, /) -> None:
        self.name = name

    def _set_key(self, *, parent_key: tuple[str, ...]) -> None:
        key = *parent_key, self.name
        # Replace with `types.get_original_bases` when requiring Python >= 3.12.
        key_type = get_args(get_args(self.__orig_bases__[0])[0])  # type: ignore[attr-defined]
        assert all(arg is str for arg in key_type)
        assert len(key) == len(key_type)
        self._key = key

    @property
    def key(self) -> _Key:
        key = self._key
        assert key
        return key  # type: ignore[return-value]


class Column(_Leaf[tuple[str, str]]):
    ...


class _Leaves:
    def _set_keys(self, *, parent_key: tuple[str, ...]) -> None:
        for _, value in getmembers(self):
            if not isinstance(value, _Leaf):
                continue

            value._set_key(parent_key=parent_key)


class Columns(_Leaves):
    ...


class Table:
    def _set_keys(self) -> None:
        name = self.name
        assert isinstance(name, str)
        columns = self.columns
        assert isinstance(columns, Columns)
        columns._set_keys(parent_key=(name,))


class Tables:
    def __init__(self) -> None:
        for _, value in getmembers(self):
            if not isinstance(value, Table):
                continue

            value._set_keys()


class Measure(_Leaf[tuple[str]]):
    ...


class Measures(_Leaves):
    ...


class Level(_Leaf[tuple[str, str, str]]):
    ...


class Levels(_Leaves):
    ...


class Hierarchy:
    ...


class Hierarchies:
    ...


class Dimension:
    ...


class Dimensions:
    ...


class Cube:
    def __init__(self) -> None:
        for _, value in getmembers(self):
            if not isinstance(value, Table):
                continue

            value._set_keys()


class Cubes:
    ...
