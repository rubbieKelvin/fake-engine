import pygame
import typing
from fakeengine.nodes import Node
from fakeengine.signal import Signal


class KeyboardData(typing.TypedDict):
    unicode: str
    key: int
    scancode: int
    pg_event: pygame.Event


class Keyboard(Node):
    """A class for key board"""

    def __init__(self) -> None:
        super().__init__(pos=0, can_render=True)
        self.on_key_up: Signal[str, KeyboardData] = Signal()
        self.on_key_down: Signal[str, KeyboardData] = Signal()

    @property
    def can_listen(self):
        return True

    def handle_event(self, event: pygame.Event):
        handler = {pygame.KEYDOWN: self.on_key_down, pygame.KEYUP: self.on_key_up}
        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            handler[event.type].emit(
                event.unicode,
                {
                    "key": event.key,
                    "unicode": event.unicode,
                    "scancode": event.scancode,
                    "pg_event": event,
                },
            )
