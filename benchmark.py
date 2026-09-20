import subprocess
import re
import csv
import statistics
import sys
import os

# Try importing pandas and matplotlib for visualization/table saving
try:
    import pandas as pd
    import matplotlib.pyplot as plt
    HAS_PLOT_LIBS = True
except ImportError:
    HAS_PLOT_LIBS = False
    print("Notice: 'pandas' or 'matplotlib' not installed. CSV will be generated, but table/chart images will be skipped.")

K_VALUES = [50, 100, 150, 200]
TRAIN_SIZES = [500, 1000, 1500, 2000]
REPETITIONS = 5

PROGRAM = "CS585_P01_A20597307.py"
TEST_FILE = "data/test.txt"

results = []

print("Starting benchmark runs...")

for k in K_VALUES:
    for train_size in TRAIN_SIZES:
        train_file = f"TRAIN_{train_size}.txt"

        # Skip if training file doesn't exist yet
        if not os.path.exists(train_file):
            print(f"Skipping: {train_file} not found.")
            continue

        training_times = []
        tokenization_times = []

        for _ in range(REPETITIONS):
            process = subprocess.run(
                [
                    sys.executable,  # Cross-platform Python execution
                    PROGRAM,
                    str(k),
                    train_file,
                    TEST_FILE
                ],
                capture_output=True,
                text=True
            )

            output = process.stdout

            training_match = re.search(r"Training time:\s*([0-9.eE+-]+)", output)
            tokenization_match = re.search(r"Tokenization time:\s*([0-9.eE+-]+)", output)

            if training_match and tokenization_match:
                training_times.append(float(training_match.group(1)))
                tokenization_times.append(float(tokenization_match.group(1)))

        if training_times and tokenization_times:
            avg_training = statistics.mean(training_times)
            avg_tokenization = statistics.mean(tokenization_times)
            
            results.append({
                "k": k,
                "train_size": train_size,
                "avg_training_time": avg_training,
                "avg_tokenization_time": avg_tokenization
            })
            print(f"Completed K={k}, Size={train_size} | Train: {avg_training:.5f}s | Tokenize: {avg_tokenization:.5f}s")
        else:
            print(f"Warning: Could not extract timing metrics for K={k}, Size={train_size}")

# 1. Save results to CSV file
csv_filename = "BPE_ANALYSIS.csv"
with open(csv_filename, "w", newline="") as file:
    fieldnames = ["k", "train_size", "avg_training_time", "avg_tokenization_time"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"\nAnalysis finished. Raw data saved to '{csv_filename}'.")

# 2. Render and save Table View + Plot Images if libraries are available
if HAS_PLOT_LIBS and results:
    df = pd.DataFrame(results)

    # --- SAVE TABLE IMAGE ---
    fig, ax = plt.subplots(figsize=(8, len(df) * 0.35 + 1))
    ax.axis('tight')
    ax.axis('off')

    # Format numbers for clean presentation
    table_data = df.copy()
    table_data['avg_training_time'] = table_data['avg_training_time'].map('{:.6f}s'.format)
    table_data['avg_tokenization_time'] = table_data['avg_tokenization_time'].map('{:.6f}s'.format)
    
    # Rename columns for presentation
    table_data.columns = ['Merges (K)', 'Train Size (Words)', 'Avg Train Time', 'Avg Tokenize Time']

    table = ax.table(
        cellText=table_data.values,
        colLabels=table_data.columns,
        cellLoc='center',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    # Style table header
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor('#1f77b4')
            cell.get_text().set_color('white')
            cell.get_text().set_weight('bold')

    plt.title("BPE Performance Benchmark Summary Table", fontsize=12, fontweight='bold', pad=15)
    plt.savefig("bpe_summary_table.png", bbox_inches='tight', dpi=300)
    plt.close()
    print("Table view saved to 'bpe_summary_table.png'.")

    # --- SAVE TRAINING TIME PLOT ---
    plt.figure(figsize=(8, 5))
    for k_val in df['k'].unique():
        subset = df[df['k'] == k_val]
        plt.plot(subset['train_size'], subset['avg_training_time'], marker='o', linewidth=2, label=f'K = {k_val}')

    plt.title('BPE Training Time vs Training Corpus Size', fontsize=12, fontweight='bold')
    plt.xlabel('Training File Size (tokens/words)')
    plt.ylabel('Average Training Time (seconds)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('bpe_training_time.png', dpi=300)
    plt.close()
    print("Chart saved to 'bpe_training_time.png'.")