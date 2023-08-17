from typing import Any, Callable, ContextManager, Iterable
from unittest.mock import patch

from vcr.request import Request

from .cassettes import (
    CassetteManager,
    CassetteConfig,
    settings,
)


class SimulationFactory:
    """
    Provides util methods to developers when implementing various simulations
    """

    def __init__(self):
        self._patches = []
        self._using_cassette = False

        self._cassette_manager = CassetteManager()

    @property
    def patches(self) -> list[ContextManager]:
        return self._patches

    def use_cassette(
            self,
            cassette_name: str,
            exclude_match_on: Iterable[str] = None,
            include_match_on: Iterable[str] = None,
            exclude_filter_headers: Iterable[str] = None,
            allow_playback_repeats: bool = False,
    ):
        """
        Tells the simulator to replay data recorded on a cassette yaml file.
        """
        if self._using_cassette:
            raise RuntimeError("Cannot use multiple cassettes for a single simulation")
        self._using_cassette = True

        self._patches.append(
            self._cassette_manager.use_cassette(
                cassette_name=cassette_name,
                config=CassetteConfig(
                    cassette_mode=settings.CASSETTE_MODE,
                    exclude_match_on=exclude_match_on,
                    include_match_on=include_match_on,
                    exclude_filter_headers=exclude_filter_headers,
                    allow_playback_repeats=allow_playback_repeats,
                ),
            )
        )

    def mock_exception(self, target: Any, attribute: str, exception: Exception):
        """
        Tells the simulator to raise an exception when a certain function is invoked.
        """
        assert isinstance(exception, Exception)
        self._patches.append(
            patch.object(target=target, attribute=attribute, side_effect=exception)
        )

    def mock_return_value(self, target: Any, attribute: str, return_value: Any):
        """
        Tells simulator to return a specific return value when a certain function is invoked.
        """
        self._patches.append(
            patch.object(target=target, attribute=attribute, return_value=return_value)
        )

    def raise_http_error_if(
        self, condition: Callable[[Request], bool], status_code: int, body: dict = None
    ):
        """
        Tells the simulator to return the specified HTTP error code/body whenever the given condition is `True`.
        """
        assert status_code >= 400

        if body is None:
            body = dict(message="Mocked error")

        self._patches.append(
            self._cassette_manager.intercept(
                condition=condition,
                status_code=status_code,
                body=body,
            )
        )


__all__ = ("SimulationFactory",)
