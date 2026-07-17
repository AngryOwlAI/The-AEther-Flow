"""Compatibility tombstone for the split Obsidian test modules.

Miniature-repository coverage lives in ``tests.test_obsidian_wiki_unit``. The
single full-source generation-and-search acceptance lives in
``tests.test_obsidian_wiki_live``. This module intentionally defines no tests,
so legacy imports remain valid without duplicate discovery or repeated live
source-corpus extraction.
"""
