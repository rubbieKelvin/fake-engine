import pygame
import typing
from fakeengine.input.devices import HardwareWrapper

class Scene:
    """Represents a page in the application, containing nodes for rendering."""

    def __init__(self, app: "App") -> None:
        """
        Initializes a new Scene instance.

        Parameters:
            app (App): The application instance to which this page belongs.
        """
        self.app = app

    def handle_event(self, event: pygame.Event) -> typing.Literal[-1] | None:
        """
        Handles events for the page.

        Parameters:
            event (pygame.event.Event): The event to handle.
        """

    def run(self, dt: float):
        """
        Runs the page logic. You probably want to render your drawings here

        Parameters:
            dt (float): The time elapsed since the last frame, in seconds.
        """

    def init(self, app: "App", **kwargs: typing.Any):
        """Initializes the page. you can set initialization variables here.
        And call some functions like getting resources and all.
        """
        pass

    def reset(self):
        """This function is called when the page is gone from view"""
        pass


class App:
    """Represents the main application"""

    instance: "App|None" = None

    def __init__(
        self,
        width: int,
        height: int,
        *,
        flags: int = 0,
        caption: str = "Game",
        clear_color: pygame.Color = pygame.Color(0, 0, 0),
    ) -> None:
        """Initializes a new App instance.

        Parameters:
            caption (str): The caption/title of the application window.
            width (int): The width of the application window.
            height (int): The height of the application window.
            clear_color (pygame.Color): Optional. The background color of the application window.
        """

        # Only one instance of this class should be available in a single runtime
        if self.instance:
            raise Exception("Application already running")

        # Set instance
        self.instance = self

        # Initialize
        pygame.init()

        self.running = False
        self.screen = pygame.display.set_mode((width, height), flags=flags)
        pygame.display.set_caption(caption)

        self.clear_color = clear_color
        self.clock = pygame.time.Clock()
        self.scene: Scene | None = None

    @property
    def height(self) -> int:
        """Returns the screen height"""
        size = pygame.display.get_window_size()
        return size[1]

    @property
    def width(self) -> int:
        """Returns the screen width"""
        size = pygame.display.get_window_size()
        return size[0]

    def run(self, delta: float):
        """Ran in a loop"""
        if self.scene:
            self.scene.run(delta)

    def handle_event(self, event: pygame.Event) -> typing.Literal[-1] | None:
        """Handle one event"""
        HardwareWrapper.sync_all(event)
        
        if self.scene:
            return self.scene.handle_event(event)
        return None

    def set_scene(self, scene: Scene | type[Scene], **kwargs: typing.Any):
        """
        Sets the current scene of the application.

        Parameters:
            scene (Scene): The scene to set as the current scene.
        """
        # reset the old scene if it exists
        if self.scene:
            self.scene.reset()

        # if we passed in a Class and not instance of a class, let's create the instance here
        if type(scene) is type:
            scene = scene(self)

        scene = typing.cast(Scene, scene)

        # run initialisation
        scene.init(self, **kwargs)
        self.scene = scene

    def mainloop(self):
        """Starts the main loop of the application."""
        self.running = True

        try:
            while self.running:
                # clear the screen
                self.screen.fill(self.clear_color)

                # event loop
                for event in pygame.event.get():
                    if self.handle_event(event) == -1:
                        break

                # frame rate limiting
                delta = self.clock.tick(60) / 1000

                self.run(delta)
                pygame.display.flip()
        except KeyboardInterrupt:
            print("Process interrupted by user.")

        # quit
        pygame.quit()
