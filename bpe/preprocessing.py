"""
preprocessing.py
----------------
Handles text cleaning, vocabulary filtering, and initial corpus tokenization.
"""

import string


def clean_file(file, initial_v):
    """
    Reads an input text file and removes non-printable characters, punctuation,
    and characters outside the allowed initial vocabulary (V).

    Args:
        file (str): Path to the input file.
        initial_v (set): Set of allowed characters (e.g., ASCII letters).

    Returns:
        str: Cleaned text string.
    """
    with open(file, 'r', encoding='utf-8', errors='ignore') as input_file:
        cnt = input_file.read()

    cln_cnt = []
    for ch in cnt:
        # Keep character if it is in initial vocabulary or space,
        # and exclude punctuation and non-printable characters.
        if (ch in initial_v or ch == " ") and ch not in string.punctuation and ch in string.printable:
            cln_cnt.append(ch)

    return "".join(cln_cnt)


def build_corpus(text):
    """
    Splits text into words and converts each word into a list of characters
    with a terminating end-of-word stop token ('_').

    Args:
        text (str): Cleaned text string.

    Returns:
        list of list of str: Tokenized corpus (e.g., [['l', 'o', 'w', '_'], ...]).
    """
    words = text.split()
    corpus = []

    for word in words:
        tokens = list(word)
        tokens.append("_")  # Append stop token to mark word boundaries
        corpus.append(tokens)

    return corpus