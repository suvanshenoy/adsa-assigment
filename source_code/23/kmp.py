try:
    from lps import compute_lps
except ImportError:
    import sys
    from pathlib import Path

    _pkg_dir = str(Path(__file__).resolve().parent)
    if _pkg_dir not in sys.path:
        sys.path.insert(0, _pkg_dir)
    from lps import compute_lps


def kmp_search(text, pattern, lps=None):

    n = len(text)
    m = len(pattern)

    # Handle an empty pattern
    if m == 0:
        raise ValueError("Pattern cannot be empty")

    # Construct LPS array if not precomputed
    if lps is None:
        lps = compute_lps(pattern)

    # Initialize pointers
    i = 0
    j = 0

    # Store matching positions
    matches = []

    # Count character comparisons
    comparisons = 0

    while i < n:

        comparisons += 1

        if text[i] == pattern[j]:

            i += 1
            j += 1

            # Complete pattern found
            if j == m:

                matches.append(i - j)

                # Continue searching for overlapping matches
                j = lps[j - 1]

        else:

            if j != 0:

                j = lps[j - 1]

            else:

                i += 1

    return matches, comparisons
