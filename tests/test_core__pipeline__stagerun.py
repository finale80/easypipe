import pytest
import functools

from enpipe import Stage, Pipeline

from typing import Callable, Any

def func_sum(a: float, b: float = 1.0) -> float:
    return a+b

def func_divide(a: float, b: float = 1.0) -> float:
    return a/b


@pytest.mark.parametrize(
    ", ".join([
        "funcs",
        "args",
        "kwargs",
        "expected_outputs"
    ]),
    [
        (
            (func_sum, func_divide), 
            (1, ), 
            dict(), 
            (
                2,
                2
            )
        ),
        (
            (
                func_sum, 
                functools.partial(func_divide, b=10),
            ), 
            tuple(),
            {"a": 10, "b": 5},
            (
                15,
                1.5
            )
        ),
    ]
)
def test_input_output(
    funcs: list[Callable],
    args: tuple[Any],
    kwargs: dict[str, Any],
    expected_outputs: Any
):
    p = Pipeline(
        *[Stage(f) for f in funcs]
    )
    p(*args, **kwargs)

    run = p.get_stages_run(0)[0]
    assert run.inputs == (args, kwargs)
    assert run.outputs == expected_outputs[0]
    for run, prev_run, exp_out in zip(
        p.get_stages_run(*list(range(1, len(p)))),
        p.get_stages_run(*list(range(0, len(p)))),
        expected_outputs[1:]
    ):
        assert run.outputs == exp_out 
        if not isinstance(prev_run.outputs, tuple):
            assert (prev_run.outputs,) == run.inputs
        else:
            assert prev_run.outputs == run.inputs
