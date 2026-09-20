"""
learner.py
----------
Implements the training phase of the Byte Pair Encoding (BPE) algorithm.
"""

import string
from .preprocessing import build_corpus
from .segmenter import merge_pair


def train_bpe(train_text, k, initial_v):
    """
    Trains the BPE model by performing K merge operations on the training corpus.

    Args:
        train_text (str): Preprocessed training text.
        k (int): Total number of merges to perform.
        initial_v (set): Base character vocabulary.

    Returns:
        tuple: (final_v, merge_rules, vocab_order)
            - final_v (set): Complete vocabulary set.
            - merge_rules (list of tuple): Ordered sequence of learned merge rules.
            - vocab_order (list of str): Ordered list of vocabulary tokens.
    """
    # Initialize vocabulary with base letters and stop token
    final_v = initial_v.copy()
    final_v.add("_")
    vocab_order = list(string.ascii_letters) + ["_"]

    # Step 1: Build initial character-level corpus
    corpus = build_corpus(train_text)
    merge_rules = []

    # Step 2: Perform up to K merges
    for _ in range(k):
        # Step 3: Count adjacent token pair frequencies
        pairs = []
        for word in corpus:
            for i in range(len(word) - 1):
                pairs.append((word[i], word[i + 1]))

        # Stop training if no adjacent pairs remain
        if not pairs:
            break

        pair_counts = {}
        for pair in pairs:
            pair_counts[pair] = pair_counts.get(pair, 0) + 1

        # Step 4: Select the pair with the maximum frequency
        new_token = max(pair_counts, key=pair_counts.get)

        # Step 5: Record rule and update vocabulary ordering
        merge_rules.append(new_token)
        merged_token = ''.join(new_token)
        final_v.add(merged_token)
        vocab_order.append(merged_token)

        # Step 6: Apply the winning merge across the corpus
        corpus = merge_pair(corpus, new_token)

    return final_v, merge_rules, vocab_order