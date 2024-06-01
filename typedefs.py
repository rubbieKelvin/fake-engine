import typing

Number = typing.TypeVar("Number", int, float)
type Factory[T] = typing.Callable[[], T]
type Polarity = typing.Literal[-1, 0, 1]
