import typing
import pygame
from . import typedefs as types
from .devices import Joystick


class BaseEventListenerMixin:
    def __init__(self) -> None:
        self.is_listening = True

    def _listen(self, event: pygame.Event): ...

    @typing.final
    def listen(self, event: pygame.Event):
        if not self.is_listening:
            return
        self._listen(event)

    @typing.final
    @staticmethod
    def group_listen(
        instance: "BaseEventListenerMixin",
        event: pygame.Event,
        *classes: type["BaseEventListenerMixin"],
    ):
        for ec in classes:
            ec.listen(instance, event)


class EventListenerMixin(BaseEventListenerMixin):

    def _modifier_args_for_key_event(self, events: pygame.Event):
        return dict(
            ctrl=bool(pygame.key.get_mods() & pygame.KMOD_CTRL),
            shift=bool(pygame.key.get_mods() & pygame.KMOD_SHIFT),
            alt=bool(pygame.key.get_mods() & pygame.KMOD_ALT),
            ctrl_l=bool(pygame.key.get_mods() & pygame.KMOD_LCTRL),
            shift_l=bool(pygame.key.get_mods() & pygame.KMOD_LSHIFT),
            alt_l=bool(pygame.key.get_mods() & pygame.KMOD_LALT),
            ctrl_r=bool(pygame.key.get_mods() & pygame.KMOD_RCTRL),
            shift_r=bool(pygame.key.get_mods() & pygame.KMOD_RSHIFT),
            alt_r=bool(pygame.key.get_mods() & pygame.KMOD_RALT),
        )

    def _listen(self, event: pygame.Event):
        match event.type:
            case pygame.MOUSEMOTION:
                self.on_mouse_motion(
                    types.MouseMotionEvent(
                        pos=pygame.Vector2(event.pos),
                        rel=pygame.Vector2(event.rel),
                        buttons=event.buttons,
                        touch=event.touch,
                    ),
                )

            case pygame.MOUSEBUTTONDOWN:
                self.on_mouse_button_down(
                    types.MouseButtonDownEvent(
                        pos=pygame.Vector2(event.pos),
                        button=event.button,
                        touch=event.touch,
                    ),
                )

            case pygame.MOUSEBUTTONUP:
                self.on_mouse_button_up(
                    types.MouseButtonUpEvent(
                        pos=pygame.Vector2(event.pos),
                        button=event.button,
                        touch=event.touch,
                    ),
                )

            case pygame.TEXTINPUT:
                self.on_text_input(
                    types.TextInputEvent(
                        text=event.text,
                        **self._modifier_args_for_key_event(event),
                    )
                )

            case pygame.KEYDOWN:
                # print(event)
                self.on_key_down(
                    types.KeyDownEvent(
                        unicode=event.unicode,
                        key=event.key,
                        mod=event.mod,
                        scancode=event.scancode,
                        **self._modifier_args_for_key_event(event),
                    )
                )

            case pygame.KEYUP:
                self.on_key_up(
                    types.KeyUpEvent(
                        unicode=event.unicode,
                        key=event.key,
                        mod=event.mod,
                        scancode=event.scancode,
                        **self._modifier_args_for_key_event(event),
                    )
                )

    def on_mouse_motion(self, event: types.MouseMotionEvent): ...
    def on_mouse_button_down(self, event: types.MouseButtonDownEvent): ...
    def on_mouse_button_up(self, event: types.MouseButtonUpEvent): ...
    def on_key_down(self, event: types.KeyDownEvent): ...
    def on_key_up(self, event: types.KeyUpEvent): ...
    def on_text_input(self, event: types.TextInputEvent): ...


class ControllerListenerMixin(BaseEventListenerMixin):
    # TODO: Finish
    # Make this class generic for all kinds of controllers
    def _listen(self, event: pygame.Event):
        match event.type:
            case pygame.JOYDEVICEADDED:
                print(event)
                # stopped here

    def on_joystick_connected(self, device: Joystick):
        pass

    def on_joystick_disconnected(self, device: Joystick):
        pass
