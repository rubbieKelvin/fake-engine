import math
import typing
import pygame
from fakeengine.app import Scene
from fakeengine.typedefs import Factory


class Node:
    """Represents a basic drawable element."""

    def __init__(self, pos: tuple[float, float]) -> None:
        """
        Initializes a new Node instance.

        Parameters:
            pos (tuple[float, float): The node's position
        """
        self.pos = pos

    def handle_event(self, event: pygame.Event):
        """Handle event"""
        pass

    def render(self, scene: "Scene") -> tuple[pygame.Surface, pygame.Vector2] | None:
        """
        Draws the node.

        Parameters:
            scene (Scene): The scene to draw the node on.

        Returns:
            tuple[Surface, Vector2] | None: A tuple containing the surface to draw and the position,
                or None if the node cannot be rendered by the scene.
        """

    def process(self, delta: float, scene: "Scene") -> None:
        """handle computations for this node"""


class Text(Node):
    def __init__(
        self,
        pos: tuple[float, float] = (0, 0),
        text: str | Factory[str] | None = None,
        font: pygame.Font | None = None,
        color: pygame.Color = pygame.Color(0, 0, 0),
        center: bool = False,
    ) -> None:
        super().__init__(pos)
        self.text = text
        self.color = color
        self.font = font or pygame.font.SysFont("DejaVu Sans", 16)
        self.center = center

    def draw(
        self, scene: "Scene", *, return_surf=True
    ) -> tuple[pygame.Surface, pygame.Vector2] | None:
        if self.text:
            text = self.text() if callable(self.text) else self.text
            surf = self.font.render(text, True, self.color)

            rect = surf.get_frect()
            rect.topleft = self.pos

            if self.center:
                rect.center = self.pos

            if return_surf:
                return surf, pygame.Vector2(rect.topleft)
            scene.app.screen.blit(surf, rect)
        return None


class Logger(Node):
    INSTANCE: 'Logger|None' = None
    
    def __init__(
        self,
        pos: tuple[float, float],
        header: str | None = "Logs",
        font: pygame.Font | None = None,
        color: pygame.Color = pygame.Color(0, 0, 0),
        cap: int = 50,
    ) -> None:
        super().__init__(pos)
        self.cap = cap
        self.header = header
        self.logs: list[str] = (
            [header.capitalize(), f"+{'-'*len(header)}"] if header else []
        )
        self.text_node = Text(pos, lambda: "\n".join(self.logs), font, color)

    @staticmethod
    def log(*args: str, sep=" "):
        if Logger.INSTANCE is None:
            return
        
        self = Logger.INSTANCE
        if len(args) == 0:
            raise Exception("At least one argument is required")

        text = sep.join(args)

        self.logs.insert(2 if self.header else 0, text)
        if len(self.logs) > self.cap:
            self.logs = self.logs[: self.cap]

    def draw(
        self,
        scene: "Scene",
    ) -> None:
        self.text_node.draw(scene, return_surf=False)


class Timer(Node):
    def __init__(
        self,
        timeout: float,
        trigger: typing.Callable[..., typing.Any],
        single_shot: bool = True,
    ) -> None:
        Node.__init__(self, (0, 0))
        self.countdown: float = 0.0
        self.timeout = timeout
        self.trigger = trigger
        self.single_shot = single_shot

    @property
    def active(self) -> bool:
        return self.countdown < self.timeout or not self.single_shot

    def reset(self):
        self.countdown = 0

    def process(self, delta: float, scene: Scene):
        if not self.active:
            return

        self.countdown += delta

        if self.countdown >= self.timeout:
            self.trigger()

            if self.single_shot:
                self.countdown = math.inf
            else:
                self.reset()
