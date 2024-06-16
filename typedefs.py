import typing
import pygame

Number = typing.TypeVar("Number", int, float)
type Factory[T] = typing.Callable[[], T]
type Polarity = typing.Literal[-1, 0, 1]
type Position = tuple[float, float] | pygame.Vector2