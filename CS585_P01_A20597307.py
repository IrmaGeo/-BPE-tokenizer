import sys
import os
import string
import pandas as pd

def validate_input(command_args):
    if len(command_args) != 4:
        print("Error: Please provide exactly 3 command line arguments.")
        sys.exit()
    k = command_args[1]
    train_file = command_args[2]
    test_file = command_args[3]

    try:
        k = int(k)

        # K must be 5
        if k != 5:
            print("K must be 5")
    except ValueError:
        print("K must be an integer")

    if not os.path.isfile(train_file):
             print ("ERROR: train file does not exist.")
             sys.exit()
    if not os.path.isfile(test_file):
                 print ("ERROR: test file does not exist.")
                 sys.exit()

def clean_train_file(file, initial_V):

    # read file
    with open(file, 'r') as input_file:
        cnt = input_file.read()

    # remove all punctuation
    # remove all non-printable characters other than space
    # remove other characters that are NOT in the INITIAL Vocabulary V

    cln_cnt=""
    for i in range(len(cnt)):
        if (cnt[i] in initial_V or cnt[i]== " ") and cnt[i] not in string.punctuation and cnt[i] in string.printable:
            cln_cnt=cln_cnt+cnt[i]
   
    return cln_cnt

def train_bpe(train_text, k, initial_V):
    # add the stop token character to your vocabulary

    final_V = initial_V.copy()
    final_V.add("_")

    # step 1: split words by space
    corpus=train_text.split()

    # step 2: for each word add stop token at the end
    suffix="_"
    for i in range(len(corpus)):
         corpus[i]=str(corpus[i])+suffix
    

    # for each i in range(k):
    
    # step 3: create adjacent pairs from current tokenized words
    pairs=[]
    for i in range(len(corpus)):
        for j in range(len(corpus[i])-1):
            pairs.append((corpus[i][j], corpus[i][j + 1]))
               
    # step 4: count each pair

    pair_counts={}
    max_count=0
    for pair in pairs:
        if pair in pair_counts:
            pair_counts[pair]+=1
        else:
            pair_counts[pair] = 1        

    # step 5: choose first max(count(pair)) using tie-break rule
    
    for pair in pair_counts:
        if max_count<pair_counts[pair]:
              max_count=pair_counts[pair]
              new_token=pair
      
    # step 6: add merged token to final_V

    merged_token = ''.join(new_token)
    final_V.add(merged_token)

    # step 7: merge that pair everywhere

      
    return final_V
    
command_args = sys.argv
validate_input(command_args)

# Command-line parameters
k = int(command_args[1])
train_file = command_args[2]
test_file = command_args[3]


# Initial vocabulary V:
# all uppercase and lowercase letters in the English alphabet
initial_V =set(string.ascii_letters)

# Read and clean training data
train_text = clean_train_file(train_file, initial_V)

# Train BPE model
final_V = train_bpe(train_text, k, initial_V)
# print(final_V)

# output
print("Modzgvrishvili, Irma, A20597307 solution:")
print("Number of merges: ", k)
print("Training file name: ", train_file)
print("Test file name: ", test_file)


# Training time: yyy seconds
# Tokenization time: zzz seconds
# Tokenization result: <tokenization result here>






