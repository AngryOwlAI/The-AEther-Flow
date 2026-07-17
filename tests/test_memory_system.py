"""Compatibility tombstone for the split memory-system test modules.

Fixture-backed coverage lives in ``tests.test_memory_system_unit``. The two
full-repository acceptance checks live in ``tests.test_memory_system_live``.
This module intentionally defines no tests, so legacy module imports remain
valid without duplicating discovery or reintroducing live checks into the fast
unit shard.
"""
