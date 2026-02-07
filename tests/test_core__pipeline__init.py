from __future__ import annotations

import pytest
import functools

from typing import Callable, Sequence
from functools import partial

from easypipe import Stage, Pipeline


def func_sum(a: float, b: float = 1.0) -> float:
    return a+b

def func_divide(a: float, b: float = 1.0) -> float:
    return a/b


@pytest.mark.parametrize(
    ", ".join([
        "funcs",
        "names",
    ]),
    [
        (
            (func_sum, func_divide), 
            ("func_sum", "func_divide"),
        ),
        (
            (func_sum, functools.partial(func_divide, b=0.0)),
            ("func_sum", "functools.partial(func_divide)"),
        ),
        (
            (
                functools.partial(func_sum, b=2), 
                functools.partial(func_sum, b=0.0)
            ),
            (
                "functools.partial(func_sum)_1",
                "functools.partial(func_sum)_2",
            )
        ),
        (
            (func_sum, partial(func_divide, b=0.0)),
            ("func_sum", "functools.partial(func_divide)"),
        ),
        (
            (lambda a: a + 1, lambda a: a+2),
            ("<lambda>_1", "<lambda>_2")
        )
    ]
)
def test_run(
    funcs: Sequence[Callable],
    names: Sequence[str],
):
    p = Pipeline(
        *[Stage(f) for f in funcs]
    )
    assert p.names == names

    for idx, stage in enumerate(p):
        assert stage.name == names[idx]
        assert p[idx] == stage


