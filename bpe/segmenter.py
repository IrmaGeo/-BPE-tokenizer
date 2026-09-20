"""
segmenter.py
------------
Applies learned BPE merge rules to segment test text into subword tokens.
"""

from .preprocessing import build_corpus


def merge_pair(corpus, rule):
    """
    Replaces adjacent token pairs matching a specific merge rule across the corpus.

    Args:
        corpus (list of list of str): The tokenized text dataset.
        rule (tuple of str): The pair of tokens to merge (e.g., ('t', 'h')).

    Returns:
        list of list of str: Updated corpus with merged tokens.
    """
    merged_token = ''.join(rule)

    for word in corpus:
        token_index = 0
        while token_index < len(word) - 1:
            if (word[token_index], word[token_index + 1]) == rule:
                word[token_index] = merged_token
                del word[token_index + 1]
            else:
                token_index += 1

    return corpus


def tokenized_data(text, rules):
    """
    Tokenizes raw text by sequentially applying learned BPE merge rules.

    Args:
        text (str): Cleaned text to tokenize.
        rules (list of tuple): Ordered sequence of merge rules from training.

    Returns:
        list of list of str: Segmented corpus.
    """
    corpus = build_corpus(text)

    # Apply merge rules sequentially in exact order learned
    for rule in rules:
        corpus = merge_pair(corpus, rule)

    return corpus