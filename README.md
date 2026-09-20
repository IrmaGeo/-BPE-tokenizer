# CS585 Programming Assignment 1 — BPE Tokenizer

## Overview

This project implements a simple **Byte-Pair Encoding (BPE)** tokenizer in Python for CS 585 Natural Language Processing.

The program:

- validates command-line arguments
- reads and cleans training and test files
- builds the initial vocabulary
- trains a BPE learner for `K` merge operations
- stores learned merge rules
- tokenizes the test file with the trained BPE segmenter
- saves the final vocabulary and tokenization result
- reports training and tokenization execution times

A separate analysis script is used to benchmark the tokenizer for different values of `K` and training-file sizes.

## Main Program

Main file:

```text
CS585_P01_A20597307.py
```

### Run the program

```bash
python CS585_P01_A20597307.py K TRAIN_FILE TEST_FILE
```

Example:

```bash
python CS585_P01_A20597307.py 50 TRAIN_500.txt test.txt
```

Arguments:

- `K` — number of BPE merge operations
- `TRAIN_FILE` — training text file
- `TEST_FILE` — test text file

Both input files must be in the same directory as the Python program.

## Input Validation

The program checks that:

- exactly three command-line arguments are provided
- `K` can be converted to an integer
- if `K <= 0` or is not an integer, `K = 5` is used
- the training file exists
- the test file exists

## Initial Vocabulary

The initial vocabulary contains all uppercase and lowercase English letters:

```text
a-z
A-Z
```

The stop token `_` is added before BPE training.

## Text Preprocessing

The training and test files are cleaned before processing.

The preprocessing step:

- removes punctuation
- removes non-printable characters
- removes characters not in the initial vocabulary
- keeps normal spaces for word tokenization

Each file is treated as one continuous text input.

## Corpus Representation

The cleaned text is split into words. Each word is converted into a list of characters and the stop token `_` is added at the end.

Example:

```text
love
```

becomes:

```python
['l', 'o', 'v', 'e', '_']
```

## BPE Training

For each BPE merge iteration, the program:

1. creates all adjacent token pairs
2. counts pair frequencies
3. selects the most frequent pair
4. records the selected merge rule
5. adds the merged token to the final vocabulary
6. merges the selected pair everywhere in the training corpus

Example:

```text
('o', 'v') -> 'ov'
```

The learned merge rules are stored in order and later used by the BPE segmenter.

## BPE Segmentation

The test file is cleaned and converted to the same corpus representation as the training file.

The segmenter applies the learned merge rules to the test corpus in the same order in which they were learned.

No new pair frequencies are calculated during test tokenization.

## Output Files

### Final Vocabulary

```text
CS585_P01_A20597307_VOCAB.txt
```

The vocabulary is saved one token per line in vocabulary/merge order.

### Tokenization Result

```text
CS585_P01_A20597307_RESULT.txt
```

The complete tokenized test text is saved with spaces used as token separators.

## Console Output

The program displays:

```text
Modzgvrishvili, Irma, A20597307 solution:
Number of merges: ...
Training file name: ...
Test file name: ...
Training time: ...
Tokenization time: ...
Tokenization result: ...
```

If the tokenized result contains more than 20 tokens, only the first 20 are displayed, followed by:

```text
Tokenized text is longer than 20 tokens
```

The complete tokenization is still saved in the result file.

## Runtime Measurement

Execution time is measured using:

```python
time.perf_counter()
```

### Training Time

Measures only BPE training:

```text
train_bpe(...)
```

Preprocessing time is excluded.

### Tokenization Time

Measures only BPE segmentation:

```text
tokenized_data(...)
```

Preprocessing time is excluded.

# Benchmark / Analysis Script

A separate analysis script runs the tokenizer for multiple values of `K` and training-file sizes.

Suggested file name:

```text
benchmark.py
```

## Experiment Settings

Values of `K`:

```text
50, 100, 150, 200
```

Training-file sizes:

```text
500, 1000, 1500, 2000 words
```

Each configuration is repeated 5 times.

Total runs:

```text
4 K values × 4 training sizes × 5 repetitions = 80 runs
```

## Run the Analysis

```bash
python benchmark.py
```

The analysis script automatically runs the main BPE program for all combinations.

Expected files:

```text
TRAIN_500.txt
TRAIN_1000.txt
TRAIN_1500.txt
TRAIN_2000.txt
test.txt
```

## Analysis Output

Raw benchmark results are saved to:

```text
BPE_ANALYSIS.csv
```

The CSV contains:

```text
k
train_size
avg_training_time
avg_tokenization_time
```

If `pandas` and `matplotlib` are installed, the analysis script also creates:

```text
bpe_summary_table.png
bpe_training_time.png
```

## Optional Analysis Libraries

The main BPE tokenizer uses only standard Python libraries.

For analysis tables and plots:

```bash
pip install pandas matplotlib
```

If these packages are unavailable, the CSV benchmark results are still generated.

## Example Project Structure

```text
bpe-tokenizer/
│
├── bpe/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── core.py
│   ├── learner.py
│   └── segmenter.py
│
├── main.py
├── benchmark.py
├── README.md
│
├── data/
│   ├── train_500.txt
│   ├── train_1000.txt
│   ├── train_1500.txt
│   ├── train_2000.txt
│   └── test.txt
│
└── results/
    ├── vocabulary.txt
    ├── tokenized_result.txt
    ├── bpe_analysis.csv
    └── plots/
```

## Notes

- BPE learns frequent adjacent token combinations from the training corpus.
- Increasing `K` generally creates larger subword tokens.
- Training time generally increases with both `K` and training corpus size.
- Tokenization is much faster than training because it only applies already learned merge rules.
