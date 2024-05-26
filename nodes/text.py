import typing
from . import Node
from fakeengine.typedefs import Factory
from pygame.font import Font, SysFont
from pygame import Color, Surface, Vector2


if typing.TYPE_CHECKING:
    from fakeengine.app import Scene


class Text(Node):
    def __init__(
        self,
        pos: Vector2,
        text: str | Factory[str] | None = None,
        font: Font | None = None,
        color: Color = Color(0, 0, 0),
    ) -> None:
        super().__init__(pos)
        self.text = text
        self.color = color
        self.font = font or SysFont("DejaVu Sans", 16)

    def draw(self, scene: "Scene") -> tuple[Surface, Vector2] | None:
        if self.text:
            text = self.text() if callable(self.text) else self.text
            surf = self.font.render(text, True, self.color)
            return surf, self.pos
        return None
