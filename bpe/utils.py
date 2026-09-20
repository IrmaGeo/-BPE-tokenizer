"""
utils.py
--------
Utility functions for CLI validation, file output saving, and terminal display formatting.
"""

import sys
import os


def validate_input(command_args):
    """
    Validates command-line arguments passed to the script.

    Args:
        command_args (list): sys.argv list.

    Returns:
        tuple: (k, train_file, test_file)
    """
    if len(command_args) != 4:
        print("Error: Please provide exactly 3 command line arguments: <K> <TRAIN_FILE> <TEST_FILE>")
        sys.exit(1)

    k = command_args[1]
    train_file = command_args[2]
    test_file = command_args[3]

    try:
        k = int(k)
        if k <= 0:
            k = 5  # Fallback to default K if range is invalid
    except ValueError:
        k = 5

    if not os.path.isfile(train_file):
        print(f"ERROR: Train file '{train_file}' does not exist.")
        sys.exit(1)

    if not os.path.isfile(test_file):
        print(f"ERROR: Test file '{test_file}' does not exist.")
        sys.exit(1)

    return k, train_file, test_file


def save_results(vocab_order, result_tokens, output_dir="results"):
    """
    Saves the final vocabulary and tokenized output into target result text files.

    Args:
        vocab_order (list of str): Ordered vocabulary list.
        result_tokens (list of str): Tokenized output tokens.
        output_dir (str): Directory where outputs are written.
    """
    os.makedirs(output_dir, exist_ok=True)

    vocab_path = os.path.join(output_dir, "vocabulary.txt")
    result_path = os.path.join(output_dir, "tokenized_result.txt")

    with open(vocab_path, "w", encoding="utf-8") as vocab_file:
        for token in vocab_order:
            vocab_file.write(token + "\n")

    with open(result_path, "w", encoding="utf-8") as result_file:
        result_file.write(" ".join(result_tokens))


def print_output(k, train_file, test_file, training_time, tokenization_time, result_tokens):
    """
    Displays execution statistics and preview tokens in the console output.
    """
    print("\nBPE Tokenizer Execution Summary")
    print("================================")
    print("Number of merges (K):", k)
    print("Training file name:", train_file)
    print("Test file name:", test_file)
    print(f"Training time: {training_time:.6f} seconds")
    print(f"Tokenization time: {tokenization_time:.6f} seconds")

    if len(result_tokens) > 20:
        print("Tokenization result:", " ".join(result_tokens[:20]))
        print("(Tokenized text is longer than 20 tokens)")
    else:
        print("Tokenization result:", " ".join(result_tokens))