"""
Unit tests for Knuth-Morris-Pratt (KMP) and LPS array construction.
Student: USN 23 (Group 6)

Validates KMP against Python reference string search functionality across:
1. Successful pattern matching
2. Unsuccessful pattern matching
3. Multiple occurrences
4. Overlapping occurrences
5. Patterns at the beginning of a title
6. Patterns at the end of a title
7. Patterns equal to the entire title
8. Unicode and multilingual inputs (Tulu, Kannada, English)
9. Boundary cases: empty patterns, pattern longer than text, single characters.
"""

import sys
import unittest
from pathlib import Path

# Add source_code/23 to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_23 = REPO_ROOT / "source_code" / "23"
if str(SRC_23) not in sys.path:
    sys.path.insert(0, str(SRC_23))

from lps import compute_lps
from kmp import kmp_search


def reference_find_all(text, pattern):
    """
    Python reference search finding all 0-based occurrences
    with support for overlapping matches.
    """
    if not pattern:
        return []
    matches = []
    start = 0
    while True:
        pos = text.find(pattern, start)
        if pos == -1:
            break
        matches.append(pos)
        start = pos + 1
    return matches


class TestLPSConstruction(unittest.TestCase):
    """Test suite for LPS (Longest Proper Prefix which is also Suffix) array construction."""

    def test_empty_pattern(self):
        self.assertEqual(compute_lps(""), [])

    def test_single_char(self):
        self.assertEqual(compute_lps("A"), [0])

    def test_all_same_chars(self):
        self.assertEqual(compute_lps("AAAA"), [0, 1, 2, 3])

    def test_no_prefix_suffix(self):
        self.assertEqual(compute_lps("ABCDE"), [0, 0, 0, 0, 0])

    def test_classic_examples(self):
        self.assertEqual(compute_lps("ABABC"), [0, 0, 1, 2, 0])
        self.assertEqual(compute_lps("AABAACAABAA"), [0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 5])

    def test_unicode_kannada_lps(self):
        # "ಕನ್ನಡಕ" -> pattern with repeating prefix/suffix
        pat = "ಕನ್ನಡಕ"
        lps = compute_lps(pat)
        self.assertEqual(len(lps), len(pat))
        self.assertEqual(lps[0], 0)
        self.assertEqual(lps[-1], 1)


class TestKMPSearch(unittest.TestCase):
    """Test suite for KMP string search algorithm."""

    def test_successful_matching(self):
        text = "DATASTRUCTURES"
        pattern = "STRUCT"
        matches, comps = kmp_search(text, pattern)
        ref = reference_find_all(text, pattern)
        self.assertEqual(matches, [4])
        self.assertEqual(matches, ref)
        self.assertGreater(comps, 0)

    def test_unsuccessful_matching(self):
        text = "DATASTRUCTURES"
        pattern = "ALGORITHM"
        matches, comps = kmp_search(text, pattern)
        ref = reference_find_all(text, pattern)
        self.assertEqual(matches, [])
        self.assertEqual(matches, ref)
        self.assertGreater(comps, 0)

    def test_multiple_occurrences(self):
        text = "ABABA_ABABA"
        pattern = "ABA"
        matches, _ = kmp_search(text, pattern)
        ref = reference_find_all(text, pattern)
        self.assertEqual(matches, [0, 2, 6, 8])
        self.assertEqual(matches, ref)

    def test_overlapping_occurrences(self):
        text = "AAAAA"
        pattern = "AAA"
        matches, _ = kmp_search(text, pattern)
        ref = reference_find_all(text, pattern)
        self.assertEqual(matches, [0, 1, 2])
        self.assertEqual(matches, ref)

    def test_pattern_at_beginning(self):
        text = "PREFIX_SEARCH_STRING"
        pattern = "PREFIX"
        matches, _ = kmp_search(text, pattern)
        ref = reference_find_all(text, pattern)
        self.assertEqual(matches, [0])
        self.assertEqual(matches, ref)

    def test_pattern_at_end(self):
        text = "SEARCH_STRING_SUFFIX"
        pattern = "SUFFIX"
        matches, _ = kmp_search(text, pattern)
        ref = reference_find_all(text, pattern)
        self.assertEqual(matches, [14])
        self.assertEqual(matches, ref)

    def test_pattern_equals_entire_title(self):
        text = "EXACT_TITLE_MATCH"
        pattern = "EXACT_TITLE_MATCH"
        matches, _ = kmp_search(text, pattern)
        ref = reference_find_all(text, pattern)
        self.assertEqual(matches, [0])
        self.assertEqual(matches, ref)

    def test_unicode_kannada(self):
        text = "ಸೂರ್ಯಕಾಂತಿ_ಹೂವು"
        pattern = "ಕಾಂತಿ"
        matches, _ = kmp_search(text, pattern)
        ref = reference_find_all(text, pattern)
        self.assertEqual(matches, [5])
        self.assertEqual(matches, ref)

    def test_unicode_tulu(self):
        text = "ಶ್ರೀ_ಜನಾರ್ಧನ_ಮಹಾಕಾಳಿ_ದೇವಸ್ತಾನ_ಅಂಬಲಪಾಡಿ"
        pattern = "_ದೇವಸ್ತಾನ_"
        matches, _ = kmp_search(text, pattern)
        ref = reference_find_all(text, pattern)
        self.assertEqual(matches, [20])
        self.assertEqual(matches, ref)

    def test_unicode_non_matching(self):
        text = "ಮಟ್ಟು_ಗುಳ್ಳ"
        pattern = "ಬೆಂಗಳೂರು"
        matches, _ = kmp_search(text, pattern)
        ref = reference_find_all(text, pattern)
        self.assertEqual(matches, [])
        self.assertEqual(matches, ref)

    def test_pattern_longer_than_text(self):
        text = "SHORT"
        pattern = "VERY_LONG_PATTERN"
        matches, _ = kmp_search(text, pattern)
        ref = reference_find_all(text, pattern)
        self.assertEqual(matches, [])
        self.assertEqual(matches, ref)

    def test_empty_pattern_raises_value_error(self):
        text = "SOME_TEXT"
        with self.assertRaises(ValueError):
            kmp_search(text, "")

    def test_precomputed_lps(self):
        text = "ABABDABACDABABCABAB"
        pattern = "ABABCABAB"
        lps = compute_lps(pattern)
        matches, comps = kmp_search(text, pattern, lps=lps)
        ref = reference_find_all(text, pattern)
        self.assertEqual(matches, [10])
        self.assertEqual(matches, ref)


if __name__ == "__main__":
    unittest.main()
