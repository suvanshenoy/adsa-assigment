
import csv
import sys
import time
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Import KMP and LPS from Student 23
sys.path.insert(0, str(ROOT / "source_code" / "23"))

from kmp import kmp_search
from lps import compute_lps


QUERY_DIR = ROOT / "queries"
OUTPUT_DIR = ROOT / "results" / "student24"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REPEATS = 10



def naive_all_matches(text, pattern):
    """Naive algorithm that finds all overlapping matches."""

    matches = []
    comparisons = 0
    n = len(text)
    m = len(pattern)

    if m == 0:
        return matches, comparisons

    for i in range(n - m + 1):
        j = 0

        while j < m:
            comparisons += 1

            if text[i + j] != pattern[j]:
                break

            j += 1

        if j == m:
            matches.append(i)

    return matches, comparisons



def reference_all_matches(text, pattern):
    """Find all overlapping matches using Python."""

    matches = []
    start = 0

    while True:
        position = text.find(pattern, start)

        if position == -1:
            break

        matches.append(position)
        start = position + 1

    return matches


def median_time(function, repeats=REPEATS):
    """Measure execution time and return median seconds."""

    measurements = []

    # Warm-up
    function()

    for _ in range(repeats):
        start = time.perf_counter()
        function()
        end = time.perf_counter()

        measurements.append(end - start)

    return statistics.median(measurements)


def process_query(row):

    text = row["target_title"]
    pattern = row["pattern"]

    if not pattern:
        raise ValueError("Empty pattern found in workload")

    # Expected result
    expected = reference_all_matches(text, pattern)

    # Naive algorithm
    naive_matches, naive_comparisons = naive_all_matches(
        text, pattern
    )

    naive_time = median_time(
        lambda: naive_all_matches(text, pattern)
    )

    # KMP preprocessing
    lps_time = median_time(
        lambda: compute_lps(pattern)
    )

    # Construct LPS outside search timing
    lps_array = compute_lps(pattern)

    # KMP algorithm
    kmp_matches, kmp_comparisons = kmp_search(
        text, pattern, lps=lps_array
    )

    kmp_time = median_time(
        lambda: kmp_search(text, pattern, lps=lps_array)
    )

    # Correctness verification
    naive_correct = naive_matches == expected
    kmp_correct = kmp_matches == expected

    return {
        "language": row["language"],
        "sample_size": row["sample_size"],
        "pattern": pattern,
        "pattern_length": len(pattern),
        "pattern_type": row["pattern_type"],
        "naive_matches": str(naive_matches),
        "kmp_matches": str(kmp_matches),
        "naive_correct": naive_correct,
        "kmp_correct": kmp_correct,
        "naive_time_sec": naive_time,
        "kmp_time_sec": kmp_time,
        "lps_preprocessing_time_sec": lps_time,
        "naive_comparisons": naive_comparisons,
        "kmp_comparisons": kmp_comparisons,
    }


def main():

    pattern_files = sorted(QUERY_DIR.glob("*_patterns.csv"))

    if not pattern_files:
        raise FileNotFoundError(
            f"No pattern CSV files found in {QUERY_DIR}"
        )

    all_results = []

    for file_path in pattern_files:

        print(f"\nProcessing: {file_path.name}")

        with open(
            file_path,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                result = process_query(row)
                result["workload"] = file_path.stem

                all_results.append(result)

        print("Completed:", file_path.name)

    if not all_results:
        raise ValueError("No queries were processed")

    output_file = OUTPUT_DIR / "comparison_results.csv"

    with open(
        output_file,
        "w",
        encoding="utf-8",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=all_results[0].keys()
        )

        writer.writeheader()
        writer.writerows(all_results)

    total = len(all_results)

    naive_passed = sum(
        r["naive_correct"] for r in all_results
    )

    kmp_passed = sum(
        r["kmp_correct"] for r in all_results
    )

    print("\n========== BENCHMARK SUMMARY ==========")
    print("Total queries:", total)
    print(f"Naive correctness: {naive_passed}/{total}")
    print(f"KMP correctness: {kmp_passed}/{total}")

    print(
        "Average Naive comparisons:",
        round(statistics.mean(
            r["naive_comparisons"] for r in all_results
        ), 2)
    )

    print(
        "Average KMP comparisons:",
        round(statistics.mean(
            r["kmp_comparisons"] for r in all_results
        ), 2)
    )

    print("\nResults saved to:", output_file)


if __name__ == "__main__":
    main()
