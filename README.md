# Comparative Performance Analysis of Naive String Matching and Knuth-Morris-Pratt (KMP) Algorithms on Multilingual Wikipedia Titles

## 1. Assignment Title and Group Members

**Assignment Title:** Comparative Performance Analysis of Naive String Matching and Knuth-Morris-Pratt (KMP) Algorithms on Multilingual Wikipedia Titles.

**Group Number:** Group XX

**Group Members:**

| Student | Responsibility |
|---|---|
| Student 21 | Dataset sampling and pattern generation |
| Student 22 | Naive string matching algorithm implementation |
| Student 23 | KMP algorithm and LPS implementation |
| Student 24 | Correctness testing, benchmarking, graph generation and report preparation |

## 2. Dataset Filenames and Required Setup

The project uses three multilingual Wikipedia title datasets.

**Dataset filenames:**

| Language | Filename | Total Titles |
|---|---|---:|
| English | `english_titles.csv` | 19,264,252 |
| Kannada | `kannada_titles.csv` | 47,392 |
| Tulu | `tulu_titles.csv` | 4,536 |

**Dataset location:**

Place all three CSV files inside the `data/` directory.

**Required setup:**

1. Install Python on your system.
2. Install the required Python libraries.
3. Clone or download the project repository.
4. Place the datasets inside the `data/` directory.
5. Open the project folder in Visual Studio Code.
6. Run the Python scripts from the main project directory.

The `title_nfc` column is used as the search text representation. It follows Unicode NFC normalization.

## 3. Execution Instructions

Open the VS Code terminal in the main project directory.

**Step 1: Install dependencies**

```bash
pip install pandas numpy matplotlib
```

**Step 2: Validate datasets**

```bash
python check_dataset.py
```

**Step 3: Run correctness tests**

```bash
python -m unittest discover -s tests
```

**Step 4: Run Naive algorithm experiments**

Refer to the Student 22 implementation:

```text
source_code/22/
```

**Step 5: Run KMP experiments**

Refer to the Student 23 implementation:

```text
source_code/23/run_kmp_experiments.py
```

**Step 6: Run corpus-level benchmarking**

```bash
python source_code/24/student24_corpus_benchmark.py
```

**Step 7: Generate performance graphs**

```bash
python source_code/24/generate_graphs.py
```

Note: Run commands from the main project directory so that relative file paths resolve correctly. The dataset sampling script may require its configured dataset path to be aligned with the project's `data/` directory before rerunning it.

## 4. Expected Outputs

The project generates the following outputs:

- Sampled dataset CSV files for English, Kannada and Tulu.
- Matching and non-matching pattern CSV files.
- Naive algorithm experiment results.
- KMP algorithm experiment results.
- Correctness testing results.
- Benchmark summary CSV files.
- Pattern-length analysis CSV files.
- Performance comparison graphs.

**Important Student 24 output files:**

| Filename | Description |
|---|---|
| `corpus_comparison_summary.csv` | Overall benchmark results |
| `pattern_length_analysis.csv` | Performance across pattern categories |
| `weighted_pattern_category_summary.csv` | Weighted comparison summary |

**Performance graphs:**

- English character comparisons
- Kannada character comparisons
- Tulu character comparisons
- English execution time
- Kannada execution time
- Tulu execution time

The Student 24 corpus benchmark completed 2,801,152 algorithm validations with 100% validation accuracy against Python's reference substring search.

## 5. Dependencies and Environment

**Programming Language:** Python

**IDE:** Visual Studio Code

**Operating System:** Windows

**Required Python libraries:**

| Library | Purpose |
|---|---|
| pandas | CSV data handling |
| numpy | Numerical operations |
| matplotlib | Graph generation |

**Other requirements:**

- CSV dataset files
- UTF-8 / Unicode text processing
- Python terminal for script execution

The Python version and installed library versions should be recorded in `environment.txt`.

## 6. Sampling Method and Random Seed

The project uses **Reservoir Sampling** to select random samples from the Wikipedia title datasets.

This method selects a uniform random sample without loading the complete dataset into memory.

**Sampling configuration:**

- Sampling method: Reservoir Sampling
- Base random seed: `42`
- Search column: `title_nfc`
- Unicode normalization: NFC
- Empty titles are ignored.

**Random seed configuration:**

| Language | Reservoir Seed |
|---|---:|
| Tulu | 1042 |
| Kannada | 2042 |
| English | 3042 |

Smaller samples are selected from the maximum-size reservoir using separate subsample seeds.

The sampling sizes are:

- Tulu: 1,000 and 4,536 titles.
- Kannada: 1,000, 5,000, 10,000 and 25,000 titles.
- English: 1,000, 5,000, 10,000 and 25,000 titles.

The complete sampling information is recorded in `results/sampling_manifest.json`.

## 7. Reproducibility Instructions

The following steps should be followed to reproduce the experiments:

1. Use the same original English, Kannada and Tulu datasets.
2. Maintain the same dataset filenames and directory structure.
3. Install the required Python dependencies.
4. Use the same sampling method and random seeds recorded in the sampling script and manifest.
5. Generate the dataset samples and search patterns.
6. Execute the Naive and KMP algorithm implementations.
7. Run the correctness tests.
8. Execute the corpus benchmarking script.
9. Generate the performance graphs.

For consistent results, maintain the same input datasets, sampling configuration, pattern selection and experimental setup.

The Student 24 pattern selection uses random seed `2406`, with 16 patterns per language.

## 8. Limitations

1. Experiments use selected samples rather than the complete English and Kannada datasets.
2. Execution time can vary depending on hardware and background processes.
3. Pattern characteristics and match positions can influence algorithm performance.
4. KMP requires additional preprocessing to construct the LPS array.
5. Experimental results represent the tested workloads and do not establish universal performance superiority.
6. Pattern-length categories are used for comparison rather than measuring a continuous execution-time relationship for every individual pattern length.