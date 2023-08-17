from contextlib import ExitStack
from typing import Callable, ContextManager, Optional

from functools import cached_property

from .exceptions import SimulationException
from .factory import SimulationFactory
from .cassettes.vcr import VCR


def _disable_http_requests():
    """
    Context manager to prevent any HTTP requests from occurring
    in the wrapped code block.
    """
    return VCR(disable_all=True).use_cassette("unused.yaml")


class BaseSimulator:
    """
    Base class for all simulators. Used to mimic real third-party data, but uses
    mocked/recorded data.
    """

    def __init__(self, simulation_name: str):
        self.simulation_name = simulation_name
        self._stack: Optional[ExitStack] = None

    def __enter__(self):
        self._stack = ExitStack()
        self._stack.__enter__()

        # Disable all HTTP requests during simulations (even in playback mode)
        self._stack.enter_context(_disable_http_requests())

        # Add all patches from simulation method
        for patch in self.patches:
            self._stack.enter_context(patch)

    def __exit__(self, *args, **kwargs):
        self._stack.__exit__(*args, **kwargs)

    @cached_property
    def _simulation_fn(self):
        simulation_fn_name = f"simulate_{self.simulation_name}"
        simulation_fn = getattr(self, simulation_fn_name, None)

        if not isinstance(simulation_fn, Callable):
            raise SimulationException(
                f"Task {self} has no simulation method named `{simulation_fn_name}`"
            )

        return simulation_fn

    @cached_property
    def patches(self) -> list[ContextManager]:
        factory = SimulationFactory()
        self._simulation_fn(factory)
        assert (
            factory.patches
        ), f"Simulation method {self._simulation_fn} must create at least one patch"

        return factory.patches


__all__ = ("BaseSimulator",)
