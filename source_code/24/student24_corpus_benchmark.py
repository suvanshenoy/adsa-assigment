"""Student 24: corpus-level Naive vs KMP benchmark.

Uses the same fixed set of patterns per language across all available sample sizes.
Each pattern is searched independently in every title in that sampled corpus.
Titles are never concatenated. KMP LPS construction is timed separately.
"""

import csv
import random
import statistics
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
QUERY_DIR = ROOT / "queries"
SAMPLE_DIR = ROOT / "results"
OUTPUT_DIR = ROOT / "results" / "student24"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Import the existing Student 23 implementation without modifying it.
KMP_DIR = ROOT / "source_code" / "23"
sys.path.insert(0, str(KMP_DIR))
from kmp import kmp_search
from lps import compute_lps

# Five patterns from each of 2 match types x 4 pattern categories = 40 patterns.
PATTERNS_PER_STRATUM = 2
SELECTION_SEED = 2406
TIMING_REPEATS = 10


def read_csv_rows(path):
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def read_titles(path):
    titles = []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            title = row.get("title_nfc")
            if title is not None:
                titles.append(title)
    return titles


def select_fixed_patterns(language):
    """Select a reproducible, balanced pattern set from the 1,000-sample workload."""
    path = QUERY_DIR / f"{language}_1000_patterns.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing pattern workload: {path}")

    rows = read_csv_rows(path)
    strata = defaultdict(list)
    for row in rows:
        strata[(row["pattern_type"], row["pattern_category"])].append(row)

    required_types = ["matching", "non_matching"]
    required_categories = ["short", "medium", "long", "very_long"]
    rng = random.Random(SELECTION_SEED)
    selected = []

    for pattern_type in required_types:
        for category in required_categories:
            key = (pattern_type, category)
            candidates = strata.get(key, [])
            if len(candidates) < PATTERNS_PER_STRATUM:
                raise ValueError(
                    f"Not enough patterns in {language} stratum {key}: {len(candidates)}"
                )
            selected.extend(rng.sample(candidates, PATTERNS_PER_STRATUM))

    return selected


def naive_all_matches(text, pattern):
    """Naive search returning all overlapping 0-based positions and comparisons."""
    n, m = len(text), len(pattern)
    if m == 0:
        raise ValueError("Empty patterns are not supported in this experiment")

    matches = []
    comparisons = 0
    for start in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[start + j] != pattern[j]:
                break
            j += 1
        if j == m:
            matches.append(start)
    return matches, comparisons


def reference_all_matches(text, pattern):
    """Reference implementation; advances by one to include overlapping matches."""
    matches = []
    start = 0
    while True:
        position = text.find(pattern, start)
        if position == -1:
            return matches
        matches.append(position)
        start = position + 1


def run_naive_batch(titles, patterns):
    total_comparisons = 0
    for pattern in patterns:
        for title in titles:
            _, comparisons = naive_all_matches(title, pattern)
            total_comparisons += comparisons
    return total_comparisons


def run_kmp_batch(titles, patterns, lps_arrays):
    total_comparisons = 0
    for pattern, lps_array in zip(patterns, lps_arrays):
        for title in titles:
            _, comparisons = kmp_search(title, pattern, lps=lps_array)
            total_comparisons += comparisons
    return total_comparisons


def median_batch_time(function):
    # One untimed warm-up, followed by repeated whole-batch measurements.
    function()
    measurements = []
    for _ in range(TIMING_REPEATS):
        start = time.perf_counter()
        function()
        measurements.append(time.perf_counter() - start)
    return statistics.median(measurements)


def main():
    languages = ["english", "kannada", "tulu"]
    summary_rows = []
    pattern_analysis_rows = []
    validation_total = 0
    validation_passed = 0

    for language in languages:
        print(f"\n=== {language.upper()} ===")
        selected_rows = select_fixed_patterns(language)
        patterns = [row["pattern"] for row in selected_rows]
        if any(not pattern for pattern in patterns):
            raise ValueError(f"Empty pattern found for {language}")

        # Same pattern set is reused at every sample size for this language.
        sample_files = sorted(SAMPLE_DIR.glob(f"{language}_*_sample.csv"))
        if not sample_files:
            raise FileNotFoundError(f"No sample CSVs found for {language} in {SAMPLE_DIR}")

        # Construct each pattern's LPS once, and measure preprocessing separately.
        lps_start = time.perf_counter()
        lps_arrays = [compute_lps(pattern) for pattern in patterns]
        lps_total_once = time.perf_counter() - lps_start
        # Time all pattern preprocessing as a batch for a stable aggregate measure.
        lps_batch_measurements = []
        for _ in range(TIMING_REPEATS):
            start = time.perf_counter()
            [compute_lps(pattern) for pattern in patterns]
            lps_batch_measurements.append(time.perf_counter() - start)
        lps_median_total = statistics.median(lps_batch_measurements)

        for sample_path in sample_files:
            size_label = sample_path.stem.replace(f"{language}_", "").replace("_sample", "")
            titles = read_titles(sample_path)
            if not titles:
                raise ValueError(f"No titles found in {sample_path}")

            pair_count = len(titles) * len(patterns)
            print(f"Sample size {size_label}: {len(titles):,} titles x {len(patterns)} patterns = {pair_count:,} pairs")

            # One correctness/counting pass. Both algorithms get identical pairs.
            naive_comparisons = 0
            kmp_comparisons = 0
            naive_passed = 0
            kmp_passed = 0
            workload_passed = 0
            category_naive_comparisons = defaultdict(int)
            category_kmp_comparisons = defaultdict(int)
            category_pair_counts = defaultdict(int)
            for pattern, lps_array, pattern_row in zip(patterns, lps_arrays, selected_rows):
                category = pattern_row["pattern_category"]
                for title in titles:
                    expected = reference_all_matches(title, pattern)
                    naive_matches, ncomp = naive_all_matches(title, pattern)
                    kmp_matches, kcomp = kmp_search(title, pattern, lps=lps_array)
                    naive_comparisons += ncomp
                    kmp_comparisons += kcomp
                    category_naive_comparisons[category] += ncomp
                    category_kmp_comparisons[category] += kcomp
                    category_pair_counts[category] += 1
                    validation_total += 2
                    if naive_matches == expected:
                        validation_passed += 1
                        naive_passed += 1
                    if kmp_matches == expected:
                        validation_passed += 1
                        kmp_passed += 1
                    if naive_matches == expected and kmp_matches == expected:
                        workload_passed += 1

            # Search-only timings; KMP LPS arrays are precomputed outside this timing.
            naive_seconds = median_batch_time(lambda: run_naive_batch(titles, patterns))
            kmp_seconds = median_batch_time(lambda: run_kmp_batch(titles, patterns, lps_arrays))

            # Additional measurements grouped by pattern length category.
            # These timings use the same titles and the same patterns for both algorithms.
            for category in ["short", "medium", "long", "very_long"]:
                category_items = [
                    (pattern, lps_array)
                    for pattern, lps_array, pattern_row
                    in zip(patterns, lps_arrays, selected_rows)
                    if pattern_row["pattern_category"] == category
                ]
                category_patterns = [item[0] for item in category_items]
                category_lps_arrays = [item[1] for item in category_items]
                category_pairs = len(titles) * len(category_patterns)

                if not category_patterns:
                    continue

                category_naive_seconds = median_batch_time(
                    lambda: run_naive_batch(titles, category_patterns)
                )
                category_kmp_seconds = median_batch_time(
                    lambda: run_kmp_batch(titles, category_patterns, category_lps_arrays)
                )

                pattern_analysis_rows.append({
                    "language": language,
                    "sample_size_label": size_label,
                    "actual_title_count": len(titles),
                    "pattern_category": category,
                    "pattern_count": len(category_patterns),
                    "title_pattern_pairs": category_pairs,
                    "naive_total_character_comparisons": category_naive_comparisons[category],
                    "kmp_total_character_comparisons": category_kmp_comparisons[category],
                    "naive_avg_comparisons_per_pair": round(
                        category_naive_comparisons[category] / category_pairs, 6
                    ),
                    "kmp_avg_comparisons_per_pair": round(
                        category_kmp_comparisons[category] / category_pairs, 6
                    ),
                    "naive_median_batch_search_seconds": category_naive_seconds,
                    "kmp_median_batch_search_seconds": category_kmp_seconds,
                    "naive_median_search_microseconds_per_pair": (
                        category_naive_seconds * 1e6 / category_pairs
                    ),
                    "kmp_median_search_microseconds_per_pair": (
                        category_kmp_seconds * 1e6 / category_pairs
                    ),
                    "timing_repeats": TIMING_REPEATS,
                })

            row = {
                "language": language,
                "sample_size_label": size_label,
                "actual_title_count": len(titles),
                "pattern_count": len(patterns),
                "title_pattern_pairs": pair_count,
                "patterns_per_stratum": PATTERNS_PER_STRATUM,
                "pattern_selection_seed": SELECTION_SEED,
                "timing_repeats": TIMING_REPEATS,
                "both_algorithms_correct_pairs": workload_passed,
                "total_title_pattern_pairs": pair_count,
                "naive_correct_pairs": naive_passed,
                "kmp_correct_pairs": kmp_passed,
                "naive_correctness_percent": round(100 * naive_passed / pair_count, 4),
                "kmp_correctness_percent": round(100 * kmp_passed / pair_count, 4),
                "naive_total_character_comparisons": naive_comparisons,
                "kmp_total_character_comparisons": kmp_comparisons,
                "naive_avg_comparisons_per_pair": round(naive_comparisons / pair_count, 6),
                "kmp_avg_comparisons_per_pair": round(kmp_comparisons / pair_count, 6),
                "naive_median_batch_search_seconds": naive_seconds,
                "kmp_median_batch_search_seconds": kmp_seconds,
                "naive_median_search_microseconds_per_pair": naive_seconds * 1e6 / pair_count,
                "kmp_median_search_microseconds_per_pair": kmp_seconds * 1e6 / pair_count,
                "kmp_lps_batch_median_seconds": lps_median_total,
                "kmp_lps_median_microseconds_per_pattern": lps_median_total * 1e6 / len(patterns),
                "kmp_lps_total_seconds_one_pass": lps_total_once,
                "pattern_categories": "short;medium;long;very_long",
                "match_types": "matching;non_matching",
                "timing_scope": "all selected patterns searched independently against every sampled title; LPS excluded from KMP search time",
            }
            summary_rows.append(row)
            print(f"  Valid pairs: {workload_passed:,}/{pair_count:,}; Naive {naive_seconds:.4f}s; KMP {kmp_seconds:.4f}s")

    out_csv = OUTPUT_DIR / "corpus_comparison_summary.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    pattern_analysis_csv = OUTPUT_DIR / "pattern_length_analysis.csv"
    if pattern_analysis_rows:
        with pattern_analysis_csv.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(
                file, fieldnames=list(pattern_analysis_rows[0].keys())
            )
            writer.writeheader()
            writer.writerows(pattern_analysis_rows)
        print(f"Pattern-length analysis saved: {pattern_analysis_csv}")

    print("\n========== STUDENT 24 CORPUS BENCHMARK ==========")
    print(f"Workload summary rows: {len(summary_rows)}")
    print(f"Algorithm validations passed: {validation_passed:,}/{validation_total:,}")
    print(f"Validation accuracy: {100 * validation_passed / validation_total:.4f}%")
    print(f"Saved: {out_csv}")
    if validation_passed != validation_total:
        raise SystemExit("Validation failures detected. Do not use these results in the report.")


if __name__ == "__main__":
    main()
