
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

sys.path.insert(0, str(ROOT / "22"))
sys.path.insert(0, str(ROOT / "source_code" / "23"))

from naive import naive_search
from kmp import kmp_search


def naive_all_matches(text, pattern):
    """Find all overlapping matches using the Naive algorithm."""

    matches = []
    comparisons = 0
    start = 0

    while start <= len(text) - len(pattern):

        position, count = naive_search(text[start:], pattern)
        comparisons += count

        if position == -1:
            break

        actual_position = start + position
        matches.append(actual_position)

        # Advance by one to allow overlapping matches
        start = actual_position + 1

    return matches, comparisons


def reference_all_matches(text, pattern):
    """Python reference implementation."""

    matches = []
    start = 0

    while True:
        position = text.find(pattern, start)

        if position == -1:
            break

        matches.append(position)
        start = position + 1

    return matches


test_cases = [
    ("AAAAA", "AAA"),
    ("DATASTRUCTURES", "STRUCT"),
    ("ABABABAB", "ABAB"),
    ("HELLO WORLD", "WORLD"),
    ("PYTHON", "JAVA"),
    ("ABCDEF", "XYZ"),
    ("BANANA", "ANA"),
]

passed = 0
failed = 0

for text, pattern in test_cases:

    naive_matches, naive_comps = naive_all_matches(text, pattern)
    kmp_matches, kmp_comps = kmp_search(text, pattern)

    expected = reference_all_matches(text, pattern)

    if naive_matches == expected and kmp_matches == expected:
        print(f"PASSED: {pattern!r} -> {expected}")
        passed += 1
    else:
        print(f"FAILED: {pattern!r}")
        print("Expected:", expected)
        print("Naive:", naive_matches)
        print("KMP:", kmp_matches)
        failed += 1

print("\n========== TEST SUMMARY ==========")
print("Total:", passed + failed)
print("Passed:", passed)
print("Failed:", failed)
