"""Policy and schema tests from the research-control compatibility inventory."""

import unittest

from tests.support.research_control_shards import load_shard


def load_tests(
    loader: unittest.TestLoader,
    tests: unittest.TestSuite,
    pattern: str | None,
) -> unittest.TestSuite:
    return load_shard(loader, "policy")


if __name__ == "__main__":
    unittest.main()
