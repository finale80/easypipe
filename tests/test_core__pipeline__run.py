import pytest

from easypipe import Stage, Pipeline

from typing import Callable, Any, Sequence

def func_sum(a: float, b: float = 1.0) -> float:
    return a+b

def func_divide(a: float, b: float = 1.0) -> float:
    return a/b

def func_divide_by_zero(a: float, b: float) -> float:
    return a / 0


@pytest.mark.parametrize(
    ", ".join([
        "funcs",
        "args",
        "kwargs",
        "expected"
    ]),
    [
        ((func_sum, func_divide), (1, ), dict(), 2)
    ]
)
def test_run(
    funcs: list[Callable],
    args: tuple[Any],
    kwargs: dict[str, Any],
    expected: Any
):
    p = Pipeline(
        *[Stage(f) for f in funcs]
    )
    assert p(*args, **kwargs) == expected


@pytest.mark.parametrize(
    ", ".join([
        "funcs",
        "args",
        "kwargs",
        "err_msg"
    ]),
    [
        (
            (func_sum, func_divide_by_zero), (1, ), dict(), 
            "--> Error at stage#2(func_divide_by_zero)"
        )
    ]
)
def test_run_with_error(
    funcs: Sequence[Callable],
    args: tuple[Any],
    kwargs: dict[str, Any],
    err_msg: str
):
    p = Pipeline(
        *[Stage(f) for f in funcs]
    )
    with pytest.raises(Exception, match=r'Error at stage#') as e:
        assert p(*args, **kwargs)
    assert e.exconly().splitlines()[-1] == err_msg
