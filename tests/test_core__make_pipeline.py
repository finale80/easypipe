from __future__ import annotations

from typing import Callable, Any, Sequence

import pytest
import functools

from enpipe import make_pipeline


def func_sum(a, b=0):
    return a+b


@pytest.mark.parametrize(
    ", ".join([
        "funcs",
        "args",
        "kwargs",
        "expected"
    ]),
    [
        ((func_sum, func_sum), (1,1), dict(), 2),
        ((func_sum, functools.partial(func_sum, b=10)), (1,), dict(), 11), 
    ]
)
def test_make_pipeline(
    funcs: Sequence[Callable],
    args: tuple,
    kwargs: dict,
    expected: Any
):
    p = make_pipeline(*funcs)
    assert p(
        *args,
        **kwargs
    ) == expected
