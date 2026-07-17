"""Synthetic checkpoint fixtures loaded by the focused checkpoint shard."""

from __future__ import annotations

import unittest

from tests.fixtures.checkpoint.scenarios import CheckpointFixtureTests


def load_checkpoint_fixture_tests(
    loader: unittest.TestLoader,
) -> unittest.TestSuite:
    """Return the isolated fixture cases without broad discovery side effects."""

    return loader.loadTestsFromTestCase(CheckpointFixtureTests)


__all__ = ["load_checkpoint_fixture_tests"]
