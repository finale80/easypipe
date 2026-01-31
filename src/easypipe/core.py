from __future__ import annotations

from typing import Callable, Any

from collections import OrderedDict
from dataclasses import dataclass #, field

# import inspect
import functools


# @dataclass
# class StageSignature:
#     """
#     Helper class to introspect a function signature
#     """
#     func: Callable
#     names: list[str] = field(default_factory=list)
#     by_pos: list[str] = field(default_factory=list)
#     by_key: list[str] = field(default_factory=list)
#     by_pos_or_key: list[str] = field(default_factory=list)
#     by_pos_with_default: list[str] = field(default_factory=list)
#     by_key_with_default: list[str] = field(default_factory=list)
#     by_pos_or_key_with_default: list[str] = field(default_factory=list)
#     has_var_pos: bool = False
#     has_var_keys: bool = False
#
#     def __post_init__(self):
#         self._sig = inspect.signature(self.func)
#
#         for param_name, param_data in self._sig.parameters.items():
#             self.names.append(param_name)
#             has_default = param_data.default != inspect.Parameter.empty
#
#             match param_data.kind:
#                 case inspect.Parameter.POSITIONAL_ONLY:
#                     self.by_pos.append(param_name)
#                     if has_default:
#                         self.by_pos_with_default.append(param_name)
#                 case inspect.Parameter.POSITIONAL_OR_KEYWORD:
#                     self.by_pos_or_key.append(param_name)
#                     if has_default:
#                         self.by_pos_or_key_with_default.append(param_name)
#                 case inspect.Parameter.VAR_POSITIONAL:
#                     self.has_var_pos = True
#                 case inspect.Parameter.VAR_KEYWORD:
#                     self.has_var_keys = True
#                 case _:
#                     self.by_key.append(param_name)
#                     if param_data.default != inspect.Parameter.empty:
#                         self.by_key_with_default.append(param_name)
#
#     # @property
#     # def num_params(self) -> int:
#     #     return (
#     #         self.num_params_by_pos
#     #         + self.num_params_by_key
#     #         + self.num_params_by_pos_or_key
#     #     )
#     #
#     # @property
#     # def min_params(self) -> int:
#     #     return (
#     #         self.num_params
#     #         - len(self.by_pos_with_default)
#     #         - len(self.by_key_with_default)
#     #         - len(self.by_pos_or_key_with_default)
#     #     )
#     #
#     # @property
#     # def num_params_by_pos(self) -> int:
#     #     return len(self.by_pos)
#     #
#     # @property
#     # def num_params_by_key(self) -> int:
#     #     return len(self.by_key)
#     #
#     # @property
#     # def num_params_by_pos_or_key(self) -> int:
#     #     return len(self.by_pos_or_key)
#     #
#     # # @property
#     # # def num_only_positional_params_with_default(self) -> int:
#     # #     return len(self.by_pos_with_default)
#    
#     def validate_call_input(self, *args, **kwargs) -> None:
#         n_args = len(args)
#
#         n_by_pos = len(self.by_pos)
#         n_by_pos_def = len(self.by_pos_with_default)
#         n_by_pos_key = len(self.by_pos_or_key)
#         n_by_pos_key_def = len(self.by_pos_or_key_with_default)
#         n_remaining_args = n_args
#
#         if n_by_pos > 0:
#             expected = n_by_pos - n_by_pos_def
#             if n_args < expected:
#                 raise RuntimeError(f"{expected - n_args} missing args by position")
#             n_remaining_args -= expected
#
#         if (
#             n_remaining_args > n_by_pos_key
#             and not self.has_var_pos
#         ):
#             raise RuntimeError(f"{n_remaining_args} extra args by position")
#
#         expected = n_by_pos_key - n_by_pos_key_def
#         if n_remaining_args < expected:
#             raise RuntimeError("{expected} missing args by position or key")
#
#         valid_keys = (
#             set(
#                 (self.by_pos_or_key + self.by_key)
#                 [n_remaining_args:]
#             )
#         )
#         expected_keys = (
#             valid_keys
#             - set(self.by_pos_or_key_with_default)
#             - set(self.by_key_with_default)
#         )
#         keys = set(kwargs.keys())
#         missing = expected_keys - keys
#         if len(missing) > 0:
#             raise RuntimeError("{len(missing) missing args by key}")
#
#         extra = keys - valid_keys
#         if len(extra) > 0:
#             raise RuntimeError(f"{len(extra)} extra args by key")


@dataclass
class Stage:
    func: Callable
    name: str = ""

    def __post_init__(self) -> None:
        if self.name == "":
            if isinstance(self.func, functools.partial):
                self.name = f"functools.partial({self.func.func.__name__})"
            else:
                self.name = self.func.__name__
        # self._sig = StageSignature(self.func)
        self._args: tuple = tuple()
        self._kwargs: dict[str, Any] = dict()
        self._out: Any = None

    def __call__(self, *args, **kwargs) -> Any:
        self._args = args
        self._kwargs = kwargs
        # self._sig.validate_params(*args, ) #**kwargs)
        self._out = self.func(*args, **kwargs)
        return self._out
    
    def __repr__(self):
        return (
            f"{self.__class__.__name__}(" 
            f"name={self.name!r}, " 
            f"func={self.func.__name__}"
            ")"
        )


class Pipeline:
    def __init__(
        self, 
        *stages: Stage,
        name: str | None = None,
        # with_progress: bool = True,
        # progress_multiline: bool = True,
        # progress_reset_elapsed: bool = True,
    ):
        self._dict: dict[str, Stage] = OrderedDict()
        for stage in stages:
            self._dict[stage.name] = stage
        self.name = name if name is not None else ""
        # self.progress = progress
        # self.progress_multiline = progress_multiline
        # self.progress_reset_elapsed = progress_reset_elapsed

    @property
    def stages(self) -> tuple[Stage, ...]:
        return tuple(self._dict.values())

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(self._dict.keys())

    @property
    def num_stages(self) -> int:
        return len(self.stages)

    def __getitem__(self, key: int | str) -> Stage:
        if isinstance(key, int):
            if key >= self.num_stages:
                raise KeyError(
                    f"Cannot access stage {key} as only {self.num_stages} "
                    "are registered"
                )
            return self._dict[self.names[key]]
        if key not in self._dict:
            raise KeyError(f"Cannot access stage {key}")
        return self._dict[key]

    def _run_stage(
        self, 
        stage: Stage, 
        stage_idx: int,
        *args, 
        **kwargs
    ) -> tuple:
        try:
            res = stage(*args, **kwargs)
        except TypeError as e:
            e.add_note(f"--> Error at stage#{stage_idx}({stage.name})")
            raise e
        if res is None:
            res = tuple()
        elif not isinstance(res, tuple):
            res = (res, )
        return res
            

    def __call__(self, *args, **kwargs) -> Any:
        if self.num_stages == 0:
            return None

        next_args = self._run_stage(self.stages[0], 1, *args, **kwargs)
        for idx, stage in enumerate(self.stages[1:], start=2):
            next_args = self._run_stage(stage, idx, *next_args)

        if len(next_args) == 1:
            return next_args[0]
        return next_args


def make_pipeline(
    *funcs: Callable
) -> Pipeline:
    stages = [
        Stage(func)
        for func in funcs
    ]
    return Pipeline(*stages)
