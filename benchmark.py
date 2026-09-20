"""
benchmark.py
------------
Executes grid experiments across K merge counts and training set sizes,
logging average timings and generating performance plots in results/.
"""

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

# Benchmark settings
K_VALUES = [50, 100, 150, 200]
TRAIN_SIZES = [500, 1000, 1500, 2000]
REPETITIONS = 5

# Directory paths
PROGRAM = "main.py"
DATA_DIR = "data"
RESULTS_DIR = "results"
PLOTS_DIR = os.path.join(RESULTS_DIR, "plots")
TEST_FILE = os.path.join(DATA_DIR, "test.txt")

# Ensure results and plots output directories exist
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

results = []

print("Starting benchmark runs...")

for k in K_VALUES:
    for train_size in TRAIN_SIZES:
        train_file = os.path.join(DATA_DIR, f"train_{train_size}.txt")

        # Skip if training file doesn't exist inside data/
        if not os.path.exists(train_file):
            print(f"Skipping: '{train_file}' not found.")
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

            # Match floating-point execution times from main.py console output
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

# 1. Save benchmark metrics to CSV file inside results/
csv_filename = os.path.join(RESULTS_DIR, "bpe_analysis.csv")
with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    fieldnames = ["k", "train_size", "avg_training_time", "avg_tokenization_time"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"\nAnalysis finished. Raw data saved to '{csv_filename}'.")

# 2. Render and save Table View + Plot Images if visualization libraries are available
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

    summary_table_path = os.path.join(PLOTS_DIR, "bpe_summary_table.png")
    plt.title("BPE Performance Benchmark Summary Table", fontsize=12, fontweight='bold', pad=15)
    plt.savefig(summary_table_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Table view saved to '{summary_table_path}'.")

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
    
    chart_path = os.path.join(PLOTS_DIR, "bpe_training_time.png")
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"Chart saved to '{chart_path}'.")