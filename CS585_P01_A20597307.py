import sys
import os
import string

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
        if k not in (50, 100, 150, 200):
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

def clean_file(file, initial_V):

    # read file
    with open(file, 'r') as input_file:
        cnt = input_file.read()

    # remove all punctuation
    # remove all non-printable characters other than space
    # remove other characters that are NOT in the INITIAL Vocabulary V

    cln_cnt=""
    for ch in range(len(cnt)):
        if (cnt[ch] in initial_V or cnt[ch]== " ") and cnt[ch] not in string.punctuation and cnt[ch] in string.printable:
            cln_cnt=cln_cnt+cnt[ch]
   
    return cln_cnt

def train_bpe(train_text, k, initial_V):
    # add the stop token character to the vocabulary
    final_v = initial_V.copy()
    final_v.add("_")

    # step 1: split words by space
    words = train_text.split()
    corpus = []

    # step 2: for each word add stop token at the end
    for word in words:
        tokens = list(word)
        tokens.append("_")
        corpus.append(tokens)
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

        # step 7: merge that pair everywhere
        for word in corpus:
            i = 0

            while i < len(word) - 1:
                if (word[i], word[i + 1]) == new_token:
                    word[i] = merged_token
                    del word[i + 1]

                i += 1

    return final_v, merge_rules
    

# Command-line parameters
command_args = sys.argv
k,train_file, test_file =validate_input(command_args)


# Initial vocabulary V:
# all uppercase and lowercase letters in the English alphabet
initial_V =set(string.ascii_letters)

# Read and clean training data
train_text = clean_file(train_file, initial_V)

# Train BPE model
final_v, merge_rules = train_bpe(train_text, k, initial_V)
cleaned_test_text=clean_file(test_file, initial_V)
print("final vocabulary",final_v)
print("merge rule", merge_rules)


# output
print("Modzgvrishvili, Irma, A20597307 solution:")
print("Number of merges: ", k)
print("Training file name: ", train_file)
print("Test file name: ", test_file)


# Training time: yyy seconds
# Tokenization time: zzz seconds
# Tokenization result: <tokenization result here>






