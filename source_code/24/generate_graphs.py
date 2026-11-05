
import pandas as pd
import matplotlib.pyplot as plt
import os

# Read benchmark results
df = pd.read_csv(
    "results/student24/pattern_length_analysis.csv"
)

# Create figures folder
os.makedirs("figures", exist_ok=True)

categories = ["short", "medium", "long", "very_long"]
languages = ["English", "Kannada", "Tulu"]

# Calculate weighted averages across sample sizes
for language in languages:

    data = df[df["language"].str.lower() == language.lower()]

    summary = data.groupby("pattern_category").apply(
        lambda g: pd.Series({
            "naive_comparisons": (
                g["naive_avg_comparisons_per_pair"] *
                g["title_pattern_pairs"]
            ).sum() / g["title_pattern_pairs"].sum(),

            "kmp_comparisons": (
                g["kmp_avg_comparisons_per_pair"] *
                g["title_pattern_pairs"]
            ).sum() / g["title_pattern_pairs"].sum(),

            "naive_time": (
                g["naive_median_search_microseconds_per_pair"] *
                g["title_pattern_pairs"]
            ).sum() / g["title_pattern_pairs"].sum(),

            "kmp_time": (
                g["kmp_median_search_microseconds_per_pair"] *
                g["title_pattern_pairs"]
            ).sum() / g["title_pattern_pairs"].sum()
        })
    ).reindex(categories)

    x = range(len(categories))
    width = 0.35

    # Character comparisons graph
    plt.figure(figsize=(8, 5))

    plt.bar(
        [i - width/2 for i in x],
        summary["naive_comparisons"],
        width,
        label="Naive"
    )

    plt.bar(
        [i + width/2 for i in x],
        summary["kmp_comparisons"],
        width,
        label="KMP"
    )

    plt.xticks(x, ["Short", "Medium", "Long", "Very Long"])
    plt.xlabel("Pattern Length Category")
    plt.ylabel("Average Character Comparisons per Pair")
    plt.title(f"{language}: Character Comparisons")
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        f"figures/{language.lower()}_character_comparisons.png",
        dpi=300
    )
    plt.close()

    # Execution time graph
    plt.figure(figsize=(8, 5))

    plt.bar(
        [i - width/2 for i in x],
        summary["naive_time"],
        width,
        label="Naive"
    )

    plt.bar(
        [i + width/2 for i in x],
        summary["kmp_time"],
        width,
        label="KMP"
    )

    plt.xticks(x, ["Short", "Medium", "Long", "Very Long"])
    plt.xlabel("Pattern Length Category")
    plt.ylabel("Median Search Time per Pair (microseconds)")
    plt.title(f"{language}: Search Execution Time")
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        f"figures/{language.lower()}_search_time.png",
        dpi=300
    )
    plt.close()

print("All six graphs generated successfully!")
print("Check the figures folder.")
