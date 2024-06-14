import typing


def call_nullable[
    **Param, R
](
    func: typing.Callable[Param, R] | None, *args: Param.args, **kwargs: Param.kwargs
) -> (R | None):
    if func:
        return func(*args, **kwargs)
    return None


def call_many[
    **Param, R
](
    funcs: typing.Iterable[typing.Callable[Param, R]], *args: Param.args, **kwargs: Param.kwargs
) -> list[R]:
    r: list[R] = []
    for func in funcs:
        r.append(func(*args, **kwargs))
    return r
