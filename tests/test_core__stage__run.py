import pytest

from typing import Callable, Any

from easypipe import Stage

def func_sum(a: int, b: int = 0) -> int:
    return a+b

@pytest.mark.parametrize(
    ", ".join([
        "func",
        "args",
        "kwargs",
        "expected"
    ]),
    [
        (func_sum, (1, 1), dict(), 2),
        (func_sum, tuple(), dict(a=1, b=1), 2),
        (func_sum, (1, ), dict(), 1),
        (func_sum, tuple(), dict(a=1), 1),
    ]
)
def test_run(
    func: Callable,
    args: tuple,
    kwargs: dict[str, Any],
    expected: Any,
):
    assert Stage(func)(*args, **kwargs) == expected
