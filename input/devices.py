import pygame
import typing


class HardwareWrapper:
    __devices__: list[type["HardwareWrapper"]] = []

    def __init_subclass__(cls) -> None:
        HardwareWrapper.__devices__.append(cls)

    @staticmethod
    def sync(event: pygame.Event):
        pass

    @staticmethod
    @typing.final
    def sync_all(event: pygame.Event):
        for cls in HardwareWrapper.__devices__:
            cls.sync(event)


class Joystick(HardwareWrapper):
    """
    A base class representing a controller.

    Attributes:
        controllers (list): A list containing all instances of Joystick.
        index (int): The index of the controller in the controllers list.
        joystick (pygame.joystick.JoystickType | None): The joystick object associated with the controller.
        on_connected (Signal): A signal emitted when the controller is connected.
        on_disconnected (Signal): A signal emitted when the controller is disconnected.
    """

    controllers: list["Joystick"] = []
    controller_sync_events = [
        pygame.JOYDEVICEADDED,
        pygame.JOYDEVICEREMOVED,
    ]

    def __init__(self) -> None:
        """Initializes a new Joystick instance."""
        super().__init__()
        self._controller_index = len(self.controllers)
        self.controllers.append(self)
        self.stick: pygame.joystick.JoystickType | None = None

    @staticmethod
    def sync(event: pygame.Event):
        if not (event.type in Joystick.controller_sync_events):
            return

        # Handle hot plugging
        if event.type == pygame.JOYDEVICEADDED:
            unlinked_controller: Joystick | None = None

            # get the controller without a linked hardware
            for cnt in Joystick.controllers:
                if cnt.stick == None:
                    unlinked_controller = cnt
                    break

            if unlinked_controller == None:
                return

            unlinked_controller.stick = pygame.joystick.Joystick(
                unlinked_controller._controller_index
            )
        #  Handle unplugging
        elif event.type == pygame.JOYDEVICEREMOVED:
            # TODO: handle unpluging
            print(event)
