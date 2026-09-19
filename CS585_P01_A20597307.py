import sys
import os

def validate_input(command_args):
    if len(command_args) != 4:
        print("Error: Please provide exactly 3 command line arguments.")
        sys.exit()
    k = command_args[1]
    train_file = command_args[2]
    test_file = command_args[3]

    try:
        k = int(k)

        # K must be a positive integer
        if k <= 0:
            print("K is out of range.")
    except ValueError:
        print("K must be an integer")

command_args=sys.argv
validate_input(command_args)


