import subprocess
import re
import csv
import statistics

K_VALUES = [50, 100, 150, 200]
TRAIN_SIZES = [500, 1000, 1500, 2000]
REPETITIONS = 5

PROGRAM = "CS585_P01_A20597307.py"
TEST_FILE = "test.txt"

results = []

for k in K_VALUES:
    for train_size in TRAIN_SIZES:

        train_file = f"TRAIN_{train_size}.txt"

        training_times = []
        tokenization_times = []

        for _ in range(REPETITIONS):

            process = subprocess.run(
                [
                    "python",
                    PROGRAM,
                    str(k),
                    train_file,
                    TEST_FILE
                ],
                capture_output=True,
                text=True
            )

            output = process.stdout

            training_match = re.search(
                r"Training time:\s*([0-9.eE+-]+)",
                output
            )

            tokenization_match = re.search(
                r"Tokenization time:\s*([0-9.eE+-]+)",
                output
            )

            if training_match and tokenization_match:
                training_times.append(float(training_match.group(1)))
                tokenization_times.append(float(tokenization_match.group(1)))

        avg_training = statistics.mean(training_times)
        avg_tokenization = statistics.mean(tokenization_times)

        results.append({
            "k": k,
            "train_size": train_size,
            "avg_training_time": avg_training,
            "avg_tokenization_time": avg_tokenization
        })


with open("BPE_ANALYSIS.csv", "w", newline="") as file:

    fieldnames = [
        "k",
        "train_size",
        "avg_training_time",
        "avg_tokenization_time"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print("Analysis finished.")
print("Results saved to BPE_ANALYSIS.csv")