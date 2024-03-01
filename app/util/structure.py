from __future__ import annotations

from inspect import getmembers


class Column:
    def __init__(self, name: str, /) -> None:
        self.name = name
        self._key: tuple[str, str] | None = None

    def _set_key(self, *, parent_key: tuple[str]) -> None:
        self._key = *parent_key, self.name

    @property
    def key(self) -> tuple[str, str]:
        key = self._key
        assert key
        return key


class Columns:
    def _set_keys(self, *, parent_key: tuple[str, str]) -> None:
        for _, value in getmembers(self):
            if not isinstance(value, Level):
                continue

            value._set_key(parent_key=parent_key)  # noqa: SLF001


class Table:
    ...


class Tables:
    ...


class Measures:
    ...


class Level:
    def __init__(self, name: str, /) -> None:
        self.name = name
        self._key: tuple[str, str, str] | None = None

    def _set_key(self, *, parent_key: tuple[str, ...]) -> None:
        self._key = *parent_key, self.name

    @property
    def key(self) -> tuple[str, str, str]:
        key = self._key
        assert key
        return key


class Levels:
    def _set_keys(self, *, parent_key: tuple[str, str]) -> None:
        for _, value in getmembers(self):
            if not isinstance(value, Level):
                continue

            value._set_key(parent_key=parent_key)  # noqa: SLF001


class Hierarchy:
    _key: tuple[str, str] | None = None

    def _set_keys(self, *, parent_key: tuple[str]) -> None:
        name = self.name
        assert isinstance(name, str)
        self._key = *parent_key, name
        levels = self.levels
        assert isinstance(levels, Levels)
        levels._set_keys(parent_key=(*parent_key, name))  # noqa: SLF001

    @property
    def key(self) -> tuple[str, str]:
        key = self._key
        assert key
        return key


class Hierarchies:
    def _set_keys(self, *, parent_key: tuple[str]) -> None:
        for _, value in getmembers(self):
            if not isinstance(value, Hierarchy):
                continue

            value._set_keys(parent_key=parent_key)  # noqa: SLF001


class Dimension:
    def __init__(self) -> None:
        name = self.name
        assert isinstance(name, str)
        hierarchies = self.hierarchies
        assert isinstance(hierarchies, Hierarchies)
        hierarchies._set_keys(parent_key=(name,))  # noqa: SLF001


class Dimensions:
    ...


class Cube:
    ...


class Cubes:
    ...
