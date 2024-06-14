import pygame
from dataclasses import dataclass


class EventClass:
    __event_name__: str


@dataclass
class MouseMotionEvent(EventClass):
    __event_name__ = "on_mouse_motion"
    pos: pygame.Vector2
    rel: pygame.Vector2
    buttons: tuple[int, int, int]
    touch: bool


@dataclass
class MouseButtonDownEvent(EventClass):
    __event_name__ = "on_mouse_button_down"
    pos: pygame.Vector2
    button: int
    touch: bool


@dataclass
class MouseButtonUpEvent(EventClass):
    __event_name__ = "on_mouse_button_up"
    pos: pygame.Vector2
    button: int
    touch: bool


@dataclass
class KeyDownEvent(EventClass):
    __event_name__ = "on_keydown"
    unicode: str
    key: int
    mod: int
    scancode: int
    ctrl: bool
    shift: bool
    alt: bool
    ctrl_l: bool
    shift_l: bool
    alt_l: bool
    ctrl_r: bool
    shift_r: bool
    alt_r: bool


@dataclass
class KeyUpEvent(EventClass):
    __event_name__ = "on_keyup"
    unicode: str
    key: int
    mod: int
    scancode: int
    ctrl: bool
    shift: bool
    alt: bool
    ctrl_l: bool
    shift_l: bool
    alt_l: bool
    ctrl_r: bool
    shift_r: bool
    alt_r: bool


@dataclass
class TextInputEvent(EventClass):
    __event_name__ = "on_textinput"
    text: str
    ctrl: bool
    shift: bool
    alt: bool
    ctrl_l: bool
    shift_l: bool
    alt_l: bool
    ctrl_r: bool
    shift_r: bool
    alt_r: bool
