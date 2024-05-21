import typing

T = typing.TypeVar("T")
Factory: typing.TypeAlias = typing.Callable[[], T]