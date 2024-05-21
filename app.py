import pygame
import typing
from .nodes import Node


class Scene:
    """Represents a page in the application, containing nodes for rendering."""

    def __init__(self, app: "App") -> None:
        """
        Initializes a new Scene instance.

        Parameters:
            app (App): The application instance to which this page belongs.
        """
        self.app = app
        self.all_nodes: list["Node"] = []
        self.listening_nodes: list["Node"] = []

    def add_node(self, node: "Node"):
        """
        Adds a node to the page.

        Parameters:
            node (Node): The node to add to the page.
        """

        self.all_nodes.append(node)
        if node.can_listen:
            self.listening_nodes.append(node)

    def add_nodes(self, nodes: typing.Iterable["Node"]):
        """
        Adds multiple nodes to the page.

        Parameters:
            nodes (list[Node] | tuple[Node, ...]): The nodes to add to the page.
        """

        self.all_nodes.extend(nodes)
        self.listening_nodes.extend([node for node in nodes if node.can_listen])

    def remove_node(self, node: "Node"):
        if node.can_listen:
            try:
                index = self.listening_nodes.index(node)
                del self.listening_nodes[index]
            except ValueError as e:
                raise e

        try:
            index = self.all_nodes.index(node)
            node.on_destroy()
            del self.all_nodes[index]
        except ValueError:
            pass

    def _handle_event(self, event: pygame.Event):
        for node in self.listening_nodes:
            node.handle_event(event)
        self.handle_event(event)

    def handle_event(self, event: pygame.Event):
        """
        Handles events for the page.

        Parameters:
            event (pygame.event.Event): The event to handle.
        """
        pass

    def run(self, dt: float):
        """
        Runs the page logic.

        Parameters:
            dt (float): The time elapsed since the last frame, in seconds.
        """
        Node.render_many_nodes(self.all_nodes, dt, self)

    def init(self, app: "App", **kwargs: typing.Any):
        """Initializes the page. you can set initialization variables here.
        And call some fontions like getting resources and all.
        """
        pass

    def reset(self):
        """This function is called when the page is gone from view"""
        pass


class App:
    """Represents the main application"""

    INSTANCE: "App|None" = None

    def __init__(
        self,
        width: int,
        height: int,
        *,
        caption: str,
        flags: int = 0,
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
        if self.INSTANCE:
            raise Exception("Application already running")

        # Set instance
        self.INSTANCE = self

        # Initialize
        pygame.init()

        self.running = False
        self.screen = pygame.display.set_mode((width, height), flags=flags)
        pygame.display.set_caption(caption)
        self.clear_color = clear_color
        self.clock = pygame.time.Clock()
        self.current_page: Scene | None = None
        self.global_nodes: list["Node"] = (
            []
        )  # Hold a record of global nodes that run on the app level
        self.global_listening_nodes: list["Node"] = []

    def add_global_node(self, node: "Node", name: str | None = None):
        """
        Adds a global node to the app.

        Parameters:
            node (Node): The node to add to the page.
        """

        self.global_nodes.append(node)
        if node.can_listen:
            self.global_listening_nodes.append(node)

    def add_global_nodes(self, nodes: typing.Iterable["Node"]):
        """
        Adds multiple global nodes to the app.

        Parameters:
            nodes (list[Node] | tuple[Node, ...]): The nodes to add to the page.
        """

        self.global_nodes.extend(nodes)
        self.global_listening_nodes.extend([node for node in nodes if node.can_listen])

    def remove_node(self, node: "Node"):
        if node.can_listen:
            try:
                index = self.global_listening_nodes.index(node)
                del self.global_listening_nodes[index]
            except ValueError as e:
                raise e

        try:
            index = self.global_nodes.index(node)
            node.on_destroy()
            del self.global_nodes[index]
        except ValueError:
            pass

    def _handle_event(self, event: pygame.Event):
        for node in self.global_listening_nodes:
            node.handle_event(event)
        self.handle_event(event)

    @property
    def height(self) -> int:
        """Returns the screen height"""
        return self.screen.get_height()

    @property
    def width(self) -> int:
        """Returns the screen width"""
        return self.screen.get_width()

    def in_loop(self, delta: float):
        """Ran in a loop"""
        pass

    def handle_event(self, event: pygame.Event):
        """Handle one event"""
        pass

    def set_scene(self, page: Scene | type[Scene], **kwargs: typing.Any):
        """
        Sets the current page of the application.

        Parameters:
            page (Scene): The page to set as the current page.
        """
        if self.current_page:
            self.current_page.reset()

        if type(page) is type:
            page = page(self)

        page = typing.cast(Scene, page)

        page.init(self, **kwargs)
        self.current_page = page

    def loop(self):
        """Starts the main loop of the application."""
        self.running = True

        while self.running:
            self.screen.fill(self.clear_color)

            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    self.running = False

                if self.current_page:
                    self.current_page.handle_event(event)

                self._handle_event(event)

            delta = self.clock.tick(60) / 1000

            self.in_loop(delta)
            if self.current_page:
                self.current_page.run(delta)

            pygame.display.flip()

        # quit
        pygame.quit()
