"""Checkpoint tests from the research-control compatibility inventory."""

import unittest

from tests.fixtures.checkpoint import load_checkpoint_fixture_tests
from tests.support.research_control_shards import load_shard


def load_tests(
    loader: unittest.TestLoader,
    tests: unittest.TestSuite,
    pattern: str | None,
) -> unittest.TestSuite:
    suite = unittest.TestSuite()
    suite.addTests(load_shard(loader, "checkpoint"))
    suite.addTests(load_checkpoint_fixture_tests(loader))
    return suite


if __name__ == "__main__":
    unittest.main()
