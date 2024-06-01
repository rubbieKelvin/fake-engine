import typing
import pygame
from .typedefs import Number, Polarity


def neutralize(value: Number, step: Number) -> Number:
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


def relax(value: float, step: float) -> float:
    """reduce to zero"""

    # We want to smoothly reduce this to zero.
    if abs(value) < step:
        return 0

    # just remove the step from the value
    # we're using the polarity to decide if we should remove or add to the value to get to zero
    polarity = get_polarity(value) 
    return value - (step * polarity)


def get_polarity(value: float) -> Polarity:
    return 1 if value > 0 else -1