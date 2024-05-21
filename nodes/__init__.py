import typing
from pygame import Vector2, Surface, Event

if typing.TYPE_CHECKING:
    from pgshared.app import Scene


class Node:
    """Represents a basic drawable element."""

    def __init__(
        self, pos: float | Vector2 | tuple[float, float], can_render: bool = True
    ) -> None:
        """
        Initializes a new Node instance.

        Parameters:
            x (int): The x-coordinate of the node's position.
            y (int): The y-coordinate of the node's position.
            can_render (bool): Optional. Indicates whether the node can be rendered. Defaults to True.
        """
        self.pos = pos if isinstance(pos, Vector2) else Vector2(pos)
        self.can_render = can_render

    @property
    def can_listen(self) -> typing.Literal[True] | typing.Literal[False]:
        """Nodes should override this when the want to listen to events.
        The value of this is used when the node is added to the scene.
        changing the value after that would have no effect on the node.
        This is beacasue the scene only checks this property at that point
        """
        return False

    def handle_event(self, event: Event):
        """Handle event"""
        pass

    def render(self, scene: "Scene") -> tuple[Surface, Vector2] | None:
        """
        Draws the node.

        Parameters:
            scene (Scene): The scene to draw the node on.

        Returns:
            tuple[Surface, Vector2] | None: A tuple containing the surface to draw and the position,
                or None if the node cannot be rendered by the scene.
        """

    def process(self, delta: float, scene: "Scene") -> None:
        """handle computatations for this node"""

    def on_destroy(self):
        """called when a node is removed from the scene"""
        print("node destroyed")

    @staticmethod
    def render_many_nodes(nodes: list["Node"], delta: float, scene: "Scene"):
        group_to_draw: list[tuple[Surface, Vector2]] = []

        for node in nodes:
            node.process(delta, scene)

        for node in nodes:
            # # check if we can draw and we're visible
            # # dont draw objects that are not in the screen
            # if not node.can_render or not Rect(
            #     0, 0, scene.app.width, scene.app.height
            # ).collidepoint(node.pos):
            #     continue

            # get visual detail
            detail = node.render(scene)

            if detail:
                group_to_draw.append(detail)

        if len(group_to_draw) > 0:
            scene.app.screen.blits(group_to_draw)
