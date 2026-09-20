"""
main.py
-------
CLI entry point for running the BPE Tokenizer package.

Usage:
    python main.py <K> <TRAIN_FILE> <TEST_FILE>
"""

import sys
import time
import string
from bpe import (
    validate_input,
    clean_file,
    train_bpe,
    tokenized_data,
    save_results,
    print_output
)


def main():
    # 1. Parse and validate inputs
    k, train_file, test_file = validate_input(sys.argv)
    initial_v = set(string.ascii_letters)

    # 2. Preprocess & Train BPE Learner
    train_text = clean_file(train_file, initial_v)
    
    training_start = time.perf_counter()
    final_v, merge_rules, vocab_order = train_bpe(train_text, k, initial_v)
    training_time = time.perf_counter() - training_start

    # 3. Preprocess & Segment Test Dataset
    cleaned_test_text = clean_file(test_file, initial_v)

    tokenization_start = time.perf_counter()
    tokenized_test_text = tokenized_data(cleaned_test_text, merge_rules)
    tokenization_time = time.perf_counter() - tokenization_start

    # 4. Flatten token output array
    result_tokens = [token for word in tokenized_test_text for token in word]

    # 5. Export results to file & log output to console
    save_results(vocab_order, result_tokens)
    print_output(
        k, train_file, test_file,
        training_time, tokenization_time, result_tokens
    )


if __name__ == "__main__":
    main()