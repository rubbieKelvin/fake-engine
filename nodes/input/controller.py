import math
import pygame
import typing

from fakeengine.nodes import Node
from fakeengine.reactive import Signal, Ref


class JoyStickAxis(typing.TypedDict):
    x: float
    y: float
    angle: float


class BaseController(Node):
    """
    A base class representing a controller.

    Attributes:
        controllers (list): A list containing all instances of BaseController.
        index (int): The index of the controller in the controllers list.
        joystick (pygame.joystick.JoystickType | None): The joystick object associated with the controller.
        on_connected (Signal): A signal emitted when the controller is connected.
        on_disconnected (Signal): A signal emitted when the controller is disconnected.
    """

    controllers: list["BaseController"] = []

    def __init__(self) -> None:
        """Initializes a new BaseController instance."""

        super().__init__((0, 0))
        self.index = len(self.controllers)
        self.controllers.append(self)
        self.joystick: pygame.joystick.JoystickType | None = None

        self.on_connected: Signal[BaseController] = Signal()
        self.on_disconnected: Signal[BaseController] = Signal()

    def handle_controller_event(self, event: pygame.Event):
        """Handle controller event"""
        pass

    def handle_event(self, event: pygame.Event):
        """Handles events.

        Args:
            event (pygame.Event): The pygame event to handle.
        """
        if not (
            event.type
            in [
                pygame.JOYAXISMOTION,
                pygame.JOYBALLMOTION,
                pygame.JOYBUTTONDOWN,
                pygame.JOYBUTTONUP,
                pygame.JOYDEVICEADDED,
                pygame.JOYDEVICEREMOVED,
                pygame.JOYHATMOTION,
            ]
        ):
            return

        # Handle hot plugging
        if self.joystick and event.instance_id == self.joystick.get_instance_id():
            if event.type == pygame.JOYDEVICEREMOVED:
                self.on_disconnected.emit(self)
                self.joystick = None
                print(f"Joystick #{event.instance_id} disconnected")
            else:
                self.handle_controller_event(event)
        else:
            if event.type == pygame.JOYDEVICEADDED:
                self.joystick = pygame.joystick.Joystick(self.index)
                self.on_connected.emit(self)
                print(f"Joystick #{self.joystick.get_instance_id()} connected")

    def connected(self):
        """Checks if the controller is connected."""
        return not (self.joystick is None)


class Playstation4Controller(BaseController):
    """
    A class representing a Playstation 4 controller.
    """

    LEVER_THRESHOLD = -0.8  # ps4 pad value is from -1 (released) to 1 (full held)

    def __init__(self) -> None:
        """Initializes a new Playstation4Controller instance."""
        super().__init__()
        # function buttons
        self.on_x_button_up: Signal[Playstation4Controller] = Signal()
        self.on_x_button_down: Signal[Playstation4Controller] = Signal()
        self.on_square_button_up: Signal[Playstation4Controller] = Signal()
        self.on_square_button_down: Signal[Playstation4Controller] = Signal()
        self.on_circle_button_up: Signal[Playstation4Controller] = Signal()
        self.on_circle_button_down: Signal[Playstation4Controller] = Signal()
        self.on_triangle_button_up: Signal[Playstation4Controller] = Signal()
        self.on_triangle_button_down: Signal[Playstation4Controller] = Signal()
        # arrow buttons
        self.on_direction_up_button_down: Signal[Playstation4Controller] = Signal()
        self.on_direction_up_button_up: Signal[Playstation4Controller] = Signal()
        self.on_direction_down_button_down: Signal[Playstation4Controller] = Signal()
        self.on_direction_down_button_up: Signal[Playstation4Controller] = Signal()
        self.on_direction_left_button_down: Signal[Playstation4Controller] = Signal()
        self.on_direction_left_button_up: Signal[Playstation4Controller] = Signal()
        self.on_direction_right_button_down: Signal[Playstation4Controller] = Signal()
        self.on_direction_right_button_up: Signal[Playstation4Controller] = Signal()
        # util buttons
        self.on_ps_button_up: Signal[Playstation4Controller] = Signal()  # 5
        self.on_ps_button_down: Signal[Playstation4Controller] = Signal()  # 5
        self.on_share_button_up: Signal[Playstation4Controller] = Signal()  # 4
        self.on_share_button_down: Signal[Playstation4Controller] = Signal()  # 4
        self.on_option_button_up: Signal[Playstation4Controller] = Signal()  # 6
        self.on_option_button_down: Signal[Playstation4Controller] = Signal()  # 6
        # trackpad button
        self.on_track_pad_button_up: Signal[Playstation4Controller] = Signal()  # 15
        self.on_track_pad_button_down: Signal[Playstation4Controller] = Signal()  # 15
        # hat buttons
        self.on_l3_button_up: Signal[Playstation4Controller] = Signal()  # 7
        self.on_l3_button_down: Signal[Playstation4Controller] = Signal()  # 7
        self.on_r3_button_up: Signal[Playstation4Controller] = Signal()  # 8
        self.on_r3_button_down: Signal[Playstation4Controller] = Signal()  # 8
        # support buttons
        self.on_l1_button_up: Signal[Playstation4Controller] = Signal()  # 9
        self.on_l1_button_down: Signal[Playstation4Controller] = Signal()  # 9
        self.on_r1_button_up: Signal[Playstation4Controller] = Signal()  # 10
        self.on_r1_button_down: Signal[Playstation4Controller] = Signal()  # 10
        # joy stick
        self.on_l_axis_changed = Signal[Playstation4Controller, JoyStickAxis]()
        self.on_r_axis_changed = Signal[Playstation4Controller, JoyStickAxis]()
        # lever
        self.on_l2_value_changed = Signal[Playstation4Controller, float]()
        self.on_r2_value_changed = Signal[Playstation4Controller, float]()

        # TODO: Implement global pressed for all buttons an lever
        # same as the other signals above, but these will fire as long...
        # as the lever values is above the threshold in Playstation4Controller.LEVER_THRESHOLD
        # passed float is the delta time
        # self.on_l2_pressed: Signal[Playstation4Controller, float] = Signal()
        # self.on_r2_pressed: Signal[Playstation4Controller, float] = Signal()

        # Joystick values
        self._joystick_hat_l_value_x: Ref[float] = Ref(0)
        self._joystick_hat_l_value_y: Ref[float] = Ref(0)
        self._joystick_hat_r_value_x: Ref[float] = Ref(0)
        self._joystick_hat_r_value_y: Ref[float] = Ref(0)
        self._lever_l_value: float = 0
        self._lever_x_value: float = 0

        self._joystick_hat_l_value_x.watch(
            lambda value: self.on_l_axis_changed.emit(
                self,
                {
                    "x": value,
                    "y": self._joystick_hat_l_value_y.value,
                    "angle": math.atan2(self._joystick_hat_l_value_y.value, value),
                },
            )
        )

        self._joystick_hat_l_value_y.watch(
            lambda value: self.on_l_axis_changed.emit(
                self,
                {
                    "x": self._joystick_hat_l_value_x.value,
                    "y": value,
                    "angle": math.atan2(value, self._joystick_hat_l_value_x.value),
                },
            )
        )

        self._joystick_hat_r_value_x.watch(
            lambda value: self.on_r_axis_changed.emit(
                self,
                {
                    "x": value,
                    "y": self._joystick_hat_r_value_y.value,
                    "angle": math.atan2(self._joystick_hat_r_value_y.value, value),
                },
            )
        )

        self._joystick_hat_r_value_y.watch(
            lambda value: self.on_r_axis_changed.emit(
                self,
                {
                    "x": self._joystick_hat_r_value_x.value,
                    "y": value,
                    "angle": math.atan2(value, self._joystick_hat_r_value_x.value),
                },
            )
        )

        self.on_l2_value_changed.connect(
            lambda _, value: setattr(self, "_lever_l_value", value)
        )
        self.on_r2_value_changed.connect(
            lambda _, value: setattr(self, "_lever_r_value", value)
        )

        self._button_id_mapping: dict[
            int, tuple[Signal[Playstation4Controller], Signal[Playstation4Controller]]
        ] = {
            0: (self.on_x_button_up, self.on_x_button_down),
            1: (self.on_circle_button_up, self.on_circle_button_down),
            2: (self.on_square_button_up, self.on_square_button_down),
            3: (self.on_triangle_button_down, self.on_triangle_button_down),
            4: (self.on_share_button_up, self.on_share_button_down),
            5: (self.on_ps_button_up, self.on_ps_button_down),
            6: (self.on_option_button_up, self.on_option_button_down),
            7: (self.on_l3_button_up, self.on_l3_button_down),
            8: (self.on_r3_button_up, self.on_r3_button_down),
            9: (self.on_l1_button_up, self.on_l1_button_down),
            10: (self.on_r1_button_up, self.on_r1_button_down),
            11: (self.on_direction_up_button_up, self.on_direction_up_button_down),
            12: (self.on_direction_down_button_up, self.on_direction_down_button_down),
            13: (self.on_direction_left_button_up, self.on_direction_left_button_down),
            14: (
                self.on_direction_right_button_up,
                self.on_direction_right_button_down,
            ),
            15: (self.on_track_pad_button_up, self.on_track_pad_button_down),
        }

    def handle_controller_event(self, event: pygame.Event):
        """Handles Playstation 4 controller events.

        Args:
            event (pygame.Event): The pygame event to handle.
        """

        if event.type == pygame.JOYBUTTONUP:
            signal = self._button_id_mapping[event.button][0]
            signal.emit(self)

        elif event.type == pygame.JOYBUTTONDOWN:
            signal = self._button_id_mapping[event.button][1]
            signal.emit(self)

        if event.type == pygame.JOYAXISMOTION:
            axis = typing.cast(int, event.axis)
            value = typing.cast(float, event.value).__round__(2)

            if axis in range(0, 4):
                hat_axis = [
                    self._joystick_hat_l_value_x,
                    self._joystick_hat_l_value_y,
                    self._joystick_hat_r_value_x,
                    self._joystick_hat_r_value_y,
                ]
                hat_axis[axis].value = value

            elif axis == 4:
                self.on_l2_value_changed.emit(self, value)

            elif axis == 5:
                self.on_r2_value_changed.emit(self, value)

    # def process(self, delta: float, scene: Scene) -> None:
    #     if self._lever_l_value > Playstation4Controller.LEVER_THRESHOLD:
    #         self.on_l2_pressed.emit(self, delta)

    #     elif self._lever_x_value > Playstation4Controller.LEVER_THRESHOLD:
    #         self.on_r2_pressed.emit(self, delta)

    #     return super().process(delta, scene)
