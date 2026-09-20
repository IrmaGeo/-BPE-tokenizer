"""
utils.py
--------
Utility functions for CLI validation, file output saving, and terminal display formatting.
"""

import sys
import os


def resolve_file_path(file_path, default_dir="data"):
    """
    Helper function to resolve file paths.
    Checks if the path exists directly; if not, checks inside the default_dir folder.
    
    Args:
        file_path (str): Provided path or file name.
        default_dir (str): Fallback directory (e.g., 'data').

    Returns:
        str: Resolved existing file path.
    """
    # 1. Direct path check (e.g. user passed 'data/train_500.txt')
    if os.path.isfile(file_path):
        return file_path

    # 2. Fallback check inside data/ folder (e.g. user passed 'train_500.txt')
    fallback_path = os.path.join(default_dir, file_path)
    if os.path.isfile(fallback_path):
        return fallback_path

    return file_path  # Return original if neither exists (fails validation downstream)


def validate_input(command_args):
    """
    Validates command-line arguments passed to the script and resolves path locations.

    Args:
        command_args (list): sys.argv list.

    Returns:
        tuple: (k, train_file, test_file)
    """
    if len(command_args) != 4:
        print("Error: Please provide exactly 3 command line arguments: <K> <TRAIN_FILE> <TEST_FILE>")
        print("Usage Example: python main.py 50 data/train_500.txt data/test.txt")
        sys.exit(1)

    k = command_args[1]
    raw_train = command_args[2]
    raw_test = command_args[3]

    # Validate integer range for K
    try:
        k = int(k)
        if k <= 0:
            k = 5  # Fallback to default K if range is invalid
    except ValueError:
        k = 5

    # Resolve paths (handles both 'data/train_500.txt' and 'train_500.txt')
    train_file = resolve_file_path(raw_train)
    test_file = resolve_file_path(raw_test)

    # Validate file existence
    if not os.path.isfile(train_file):
        print(f"ERROR: Train file '{raw_train}' does not exist directly or in the 'data/' folder.")
        sys.exit(1)

    if not os.path.isfile(test_file):
        print(f"ERROR: Test file '{raw_test}' does not exist directly or in the 'data/' folder.")
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
    print("Training file path:", train_file)
    print("Test file path:", test_file)
    print(f"Training time: {training_time:.6f} seconds")
    print(f"Tokenization time: {tokenization_time:.6f} seconds")

    if len(result_tokens) > 20:
        print("Tokenization result:", " ".join(result_tokens[:20]))
        print("(Tokenized text is longer than 20 tokens)")
    else:
        print("Tokenization result:", " ".join(result_tokens))