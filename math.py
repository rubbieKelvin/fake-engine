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

    @staticmethod
    def _do_lines_intersect(p1, p2, q1, q2) -> bool:
        """Check if line segments (p1, p2) and (q1, q2) intersect.

        p1 : pygame.Vector2
            Start point of the first line segment.
        p2 : pygame.Vector2
            End point of the first line segment.
        q1 : pygame.Vector2
            Start point of the second line segment.
        q2 : pygame.Vector2
            End point of the second line segment.
        """

        def is_counter_clockwise(
            a: pygame.Vector2, b: pygame.Vector2, c: pygame.Vector2
        ) -> bool:
            return (c.y - a.y) * (b.x - a.x) > (b.y - a.y) * (c.x - a.x)

        return is_counter_clockwise(p1, q1, q2) != is_counter_clockwise(
            p2, q1, q2
        ) and is_counter_clockwise(p1, p2, q1) != is_counter_clockwise(p1, p2, q2)

    def collides_rect(self, rect: pygame.Rect | pygame.FRect) -> bool:
        """Checks if the polygon collides with a rectangle"""
        rect_polygon = Polygon2D.from_rect(rect)
        return self.collides_polygon(rect_polygon)

    def collides_point(self, point: pygame.Vector2 | tuple[float, float]) -> bool:
        """Checks if a point is inside the polygon using the ray-casting algorithm."""

        if isinstance(point, tuple):
            point = pygame.Vector2(point)

        # Ray-casting algorithm to check if the point is inside the polygon
        num_vertices = len(self.vectors)
        inside = False

        point_x, point_y = point.x, point.y
        vertex1_x, vertex1_y = self.vectors[0].x, self.vectors[0].y

        for i in range(1, num_vertices + 1):
            vertex2_x, vertex2_y = (
                self.vectors[i % num_vertices].x,
                self.vectors[i % num_vertices].y,
            )
            if point_y > min(vertex1_y, vertex2_y):
                if point_y <= max(vertex1_y, vertex2_y):
                    if point_x <= max(vertex1_x, vertex2_x):
                        if vertex1_y != vertex2_y:
                            x_intersection = (point_y - vertex1_y) * (
                                vertex2_x - vertex1_x
                            ) / (vertex2_y - vertex1_y) + vertex1_x
                        if vertex1_x == vertex2_x or point_x <= x_intersection:
                            inside = not inside
            vertex1_x, vertex1_y = vertex2_x, vertex2_y

        return inside

    def collides_polygon(self, polygon: "Polygon2D") -> bool:
        """Checks if the polygon collides with another polygon."""
        for point in polygon:
            if self.collides_point(point):
                return True

        for point in self:
            if polygon.collides_point(point):
                return True

        # Check if any edges intersect
        for i in range(len(self.vectors)):
            for j in range(len(polygon.vectors)):
                if Polygon2D._do_lines_intersect(
                    self.vectors[i],
                    self.vectors[(i + 1) % len(self.vectors)],
                    polygon.vectors[j],
                    polygon.vectors[(j + 1) % len(polygon.vectors)],
                ):
                    return True

        return False
