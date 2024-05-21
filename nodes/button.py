import typing
from . import Node

# TODO: ...
class Button(Node):
    @typing.final
    @property
    def can_listen(self):
        return True
