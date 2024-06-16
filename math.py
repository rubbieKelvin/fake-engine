import typing
import pygame
from .typedefs import Number, Polarity
from collections.abc import Iterator


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


class Polygon2D(Iterator):
    def __init__(self, *vectors: pygame.Vector2) -> None:
        self._index = 0
        self.vectors = vectors

    @staticmethod
    def create_from_lines(
        start: pygame.Vector2, *lineto: tuple[float, float]
    ) -> "Polygon2D":
        """Creates a polygon by adding vectors to a starting point"""
        coordinates: list[pygame.Vector2] = [start]
        last = start.copy()

        for direction in lineto:
            last = last.copy() + direction
            coordinates.append(last)

        return Polygon2D(*coordinates)

    @staticmethod
    def from_rect(rect: pygame.FRect | pygame.Rect) -> "Polygon2D":
        """Creates a polygon from a pygame rectangle"""
        top_left = pygame.Vector2(rect.topleft)
        top_right = pygame.Vector2(rect.topright)
        bottom_right = pygame.Vector2(rect.bottomright)
        bottom_left = pygame.Vector2(rect.bottomleft)
        return Polygon2D(top_left, top_right, bottom_right, bottom_left)

    def __len__(self):
        return len(self.vectors)

    def __getitem__(self, index):
        return self.vectors[index]

    def __next__(self):
        if self._index == len(self):
            self._index = 0
            raise StopIteration

        item = self.vectors[self._index]
        self._index += 1
        return item

    def __repr__(self) -> str:
        return self.vectors.__repr__()

    def __add__(self, other: pygame.Vector2 | tuple[float, float]):
        if not (type(other) in [pygame.Vector2, tuple]):
            raise TypeError(
                f"unsupported operand type(s) for +: 'Polygon2D' and '{type(other)}'"
            )
        return Polygon2D(*[v.copy() + other for v in self.vectors])

    def __sub__(self, other: pygame.Vector2):
        if not (type(other) in [pygame.Vector2, tuple]):
            raise TypeError(
                f"unsupported operand type(s) for +: 'Polygon2D' and '{type(other)}'"
            )
        return Polygon2D(*[v.copy() - other for v in self.vectors])
