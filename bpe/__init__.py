"""
Byte Pair Encoding (BPE) Package
================================

A modular Python package for training a Byte Pair Encoding (BPE) tokenizer
and segmenting unseen text.
"""

from .preprocessing import clean_file, build_corpus
from .learner import train_bpe
from .segmenter import tokenized_data, merge_pair
from .utils import validate_input, save_results, print_output

__all__ = [
    "clean_file",
    "build_corpus",
    "train_bpe",
    "tokenized_data",
    "merge_pair",
    "validate_input",
    "save_results",
    "print_output",
]