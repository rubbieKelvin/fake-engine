import typing
import pygame

Number = typing.TypeVar("Number", int, float)


def nuetralize(value: Number, step: Number) -> Number:
    if value > 0:
        return value - step
    return value + step


def rectToCoordinates(
    rect: pygame.Rect, padding: int = 1
) -> typing.Sequence[typing.Sequence[float]]:
    x = rect.x
    y = rect.y
    w = rect.w
    h = rect.h

    return (
        (x - (padding + 1), y - (padding + 1)),
        ((x + w) + padding, y - (padding + 1)),
        ((x + w) + padding, (y + h) + padding),
        (x - (padding + 1), (y + h) + padding),
    )
