from typing import TypeVar, Tuple

T = TypeVar("T")


def to_tuple(x: T | Tuple[T, ...]) -> Tuple[T]:
    return x if isinstance(x, tuple) else (x,)
