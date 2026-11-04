
import sys
from pathlib import Path

# Locate teammate algorithm folders
ROOT = Path(__file__).resolve().parent

sys.path.insert(0, str(ROOT / "22"))
sys.path.insert(0, str(ROOT / "source_code" / "23"))

from naive import naive_search
from kmp import kmp_search


def test_algorithms():

    test_cases = [
        ("DATASTRUCTURES", "STRUCT"),
        ("HELLO WORLD", "WORLD"),
        ("COMPUTER SCIENCE", "SCI"),
        ("AAAAA", "AAA"),
        ("PYTHON", "JAVA"),
        ("ABCDEF", "XYZ"),
        ("ಬೈರುತ್_ಸ್ಫೋಟ", "ರು"),
    ]

    passed = 0
    failed = 0

    for text, pattern in test_cases:

        # Naive algorithm
        naive_position, naive_comparisons = naive_search(
            text, pattern
        )

        # KMP algorithm
        kmp_matches, kmp_comparisons = kmp_search(
            text, pattern
        )

        # Python reference result
        expected_position = text.find(pattern)

        # First matching position from KMP
        kmp_position = kmp_matches[0] if kmp_matches else -1

        # Validate both algorithms
        if (
            naive_position == expected_position
            and kmp_position == expected_position
        ):
            print(f"PASSED: {pattern!r} in {text!r}")
            passed += 1
        else:
            print(f"FAILED: {pattern!r} in {text!r}")
            print("Expected:", expected_position)
            print("Naive:", naive_position)
            print("KMP:", kmp_position)
            failed += 1

    print("\n========== TEST SUMMARY ==========")
    print("Total tests:", passed + failed)
    print("Passed:", passed)
    print("Failed:", failed)


if __name__ == "__main__":
    test_algorithms()
