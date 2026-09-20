import sys
import os
import string
import time

def validate_input(command_args):
    if len(command_args) != 4:
        print("Error: Please provide exactly 3 command line arguments.")
        sys.exit()
    k = command_args[1]
    train_file = command_args[2]
    test_file = command_args[3]

    try:
        k = int(k)

        # If the K argument is out of the specified range, assume that the value for K is 5 
        if k <=0:
           k=5
    except ValueError:
        k=5
    
    if not os.path.isfile(train_file):
             print ("ERROR: train file does not exist.")
             sys.exit()
    if not os.path.isfile(test_file):
                 print ("ERROR: test file does not exist.")
                 sys.exit()
    return k,train_file, test_file

def clean_file(file, initial_v):

    # read file
    with open(file, 'r') as input_file:
        cnt = input_file.read()

    # remove all punctuation
    # remove all non-printable characters other than space
    # remove other characters that are NOT in the INITIAL Vocabulary V

    cln_cnt=""
    for ch_index in range(len(cnt)):
        if (cnt[ch_index] in initial_v or cnt[ch_index]== " ") and cnt[ch_index] not in string.punctuation and cnt[ch_index] in string.printable:
            cln_cnt=cln_cnt+cnt[ch_index]
   
    return cln_cnt

def build_corpus(text):
    words = text.split()
    corpus = []

    # add the stop token character end of the each word
    for word in words:
        tokens = list(word)
        tokens.append("_")
        corpus.append(tokens)

    return corpus

def merge_pair(corpus, rule):
    merged_token = ''.join(rule)

    for word in corpus:
        token_index = 0

        while token_index < len(word) - 1:
            if (word[token_index], word[token_index + 1]) == rule:
                word[token_index] = merged_token
                del word[token_index + 1]

            token_index += 1

    return corpus

def train_bpe(train_text, k, initial_v):
    # add the stop token character to the vocabulary
    final_v = initial_v.copy()
    final_v.add("_")
    vocab_order = list(string.ascii_letters)
    vocab_order.append("_")

    # step 1: build corpus
    corpus=build_corpus(train_text)

    merge_rules = []

    # perform K merges
    for _ in range(k):

        # step 3: create adjacent pairs from current tokenized words
        pairs = []

        for word_index in range(len(corpus)):
            for token_index in range(len(corpus[word_index]) - 1):
                pairs.append(
                    (
                        corpus[word_index][token_index],
                        corpus[word_index][token_index + 1]
                    )
                )

        # if there are no pairs left, stop training
        if not pairs:
            break

        # step 4: count each pair
        pair_counts = {}

        for pair in pairs:
            if pair in pair_counts:
                pair_counts[pair] += 1
            else:
                pair_counts[pair] = 1

        # step 5: choose first max(count(pair))
        max_count = 0

        for pair in pair_counts:
            if max_count < pair_counts[pair]:
                max_count = pair_counts[pair]
                new_token = pair

            merge_rules.append(new_token)

            # step 6: add merged token to final_v
            merged_token = ''.join(new_token)
            final_v.add(merged_token)
            vocab_order.append(merged_token)

        # step 7: merge that pair everywhere
        corpus = merge_pair(corpus, new_token)

    return final_v, merge_rules, vocab_order

def tokenized_data(text, rules):
    corpus=build_corpus(text)
    for rule in rules:
        corpus = merge_pair(corpus, rule)
    return corpus

def save_results(vocab_order, result_tokens):

    with open("CS585_P01_A20597307_VOCAB.txt", "w") as vocab_file:
        for token in vocab_order:
            vocab_file.write(token + "\n")

    with open("CS585_P01_A20597307_RESULT.txt", "w") as result_file:
        result_file.write(" ".join(result_tokens))

def print_output(k, train_file, test_file,
                 training_time, tokenization_time, result_tokens):

    print("Modzgvrishvili, Irma, A20597307 solution:")
    print("Number of merges:", k)
    print("Training file name:", train_file)
    print("Test file name:", test_file)
    print("Training time:", training_time)
    print("Tokenization time:", tokenization_time)

    if len(result_tokens) > 20:
        print("Tokenization result:", " ".join(result_tokens[:20]))
        print("Tokenized text is longer than 20 tokens")
    else:
        print("Tokenization result:", " ".join(result_tokens))

def main():
    command_args = sys.argv
    k, train_file, test_file = validate_input(command_args)

    initial_v = set(string.ascii_letters)

    train_text = clean_file(train_file, initial_v)

    training_start = time.perf_counter()
    final_v, merge_rules, vocab_order = train_bpe(train_text, k, initial_v)
    training_time = time.perf_counter() - training_start

    cleaned_test_text = clean_file(test_file, initial_v)

    tokenization_start = time.perf_counter()
    tokenized_test_text = tokenized_data(cleaned_test_text, merge_rules)
    tokenization_time = time.perf_counter() - tokenization_start

    result_tokens = []

    for word in tokenized_test_text:
        for token in word:
            result_tokens.append(token)

    save_results(vocab_order, result_tokens)

    print_output(
        k,
        train_file,
        test_file,
        training_time,
        tokenization_time,
        result_tokens
    )
 
if __name__ == "__main__":
    main()