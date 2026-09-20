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
    cln_cnt=""
    for i in range(len(cnt)):
        if cnt[i] not in string.punctuation:
            cln_cnt=cln_cnt+cnt[i]

    # remove all non-printable characters other than space
    # remove other characters that are NOT in the INITIAL Vocabulary V

    return cln_cnt

def train_bpe(train_text, k, initial_V):
      # add the stop token character to your vocabulary
      # train your BPE Learner by performing K merges
      return # return final vocabulary final_V
    
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
# final_V = train_bpe(train_text, k, initial_V)





