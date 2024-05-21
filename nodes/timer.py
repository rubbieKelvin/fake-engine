import math
import typing
import pygame
from . import Node
from pgshared.app import Scene


class Timer(Node):
    def __init__(
        self,
        timeout: float,
        trigger: typing.Callable[..., typing.Any],
        single_shot: bool = True,
    ) -> None:
        Node.__init__(self, pygame.Vector2(), can_render=False)
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
