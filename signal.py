import typing
import pydantic

T = typing.TypeVar("T")
Param = typing.ParamSpec("Param")


class Signal(typing.Generic[Param]):
    """
    A class representing a signal/slot mechanism for connecting callbacks to events.

    Args:
        name (str, optional): The name of the signal (for identification purposes).
    """

    def __init__(self, name: str | None = None) -> None:
        """
        Initializes a new Signal instance.

        Args:
            name (str, optional): The name of the signal.
        """
        self.callbacks: list[typing.Callable[Param, typing.Any]] = []

    def emit(self, *args: Param.args, **kwargs: Param.kwargs):
        """
        Emits the signal, invoking all connected callbacks with provided arguments and keyword arguments.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        for cb in self.callbacks:
            cb(*args, **kwargs)

    def connect(self, cb: typing.Callable[Param, typing.Any]):
        """
        Connects a callback function to the signal.

        Args:
            cb (Callable): The callback function to connect.
        """

        self.callbacks.append(cb)

    def disconnect(self, cb: typing.Callable[Param, typing.Any]):
        """
        Disconnects a previously connected callback function from the signal.

        Args:
            cb (Callable): The callback function to disconnect.
        """

        index = self.callbacks.index(cb)
        del self.callbacks[index]


class Ref(typing.Generic[T]):
    """
    A class representing a reference to a value of a generic type with signal support for value changes.

    Attributes:
        signal (Signal): A Signal instance for tracking value changes.
        watch (Callable): A shortcut to connect a callback to value change events.
    """

    class MethodCall(pydantic.BaseModel):
        """
        A data model representing a method call to be applied to the referenced value.

        Attributes:
            name (str): The name of the method to call.
            args (tuple): Tuple of positional arguments for the method.
            kwargs (dict): Dictionary of keyword arguments for the method.
            use_return_value (bool): Flag indicating whether to use the return value of the method as the new value.
        """

        name: str
        args: tuple = pydantic.Field(default_factory=tuple)
        kwargs: dict[str, typing.Any] = pydantic.Field(default_factory=dict)
        use_return_value: bool = False

    def __init__(self, value: T) -> None:
        """
        Initializes a new Ref instance with the provided value.

        Args:
            value (T): The initial value of the reference.
        """

        self.__raw__: T = value
        self.signal: Signal[T] = Signal()
        self.watch = self.signal.connect

    @property
    def value(self) -> T:
        """
        Property method returning the current value of the reference.

        Returns:
            T: The current value of the reference.
        """
        return self.__raw__

    @value.setter
    def value(self, v: T) -> None:
        """
        Property setter method to update the value of the reference.

        Args:
            v (T): The new value of the reference.
        """
        self.__raw__ = v
        self.signal.emit(self.__raw__)

    @typing.overload
    def mutate(self, val_or_method: T) -> None: ...
    @typing.overload
    def mutate(self, val_or_method: MethodCall) -> None: ...
    def mutate(self, val_or_method):
        """
        Mutates the referenced value. It can accept either a new value directly or a MethodCall object representing a method to be applied to the value.

        Args:
            val_or_method (Union[T, MethodCall]): The value or method to apply to the reference.
        """
        if type(val_or_method) is Ref.MethodCall:
            func = typing.cast(
                typing.Callable, getattr(self.__raw__, val_or_method.name)
            )
            return_value = func(*val_or_method.args, **val_or_method.kwargs)

            if val_or_method.use_return_value:
                self.value = return_value
            else:
                self.signal.emit(self.value)
            return
        self.value = val_or_method

    def __repr__(self) -> str:
        return f"Ref<{repr(self.value)}>"
