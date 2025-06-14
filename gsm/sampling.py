import json
import random
import csv
from pathlib import Path

# Configuration variables (edit these to suit your needs)
input_jsonl = Path(__file__).parent / "dataset" / "test.jsonl"      # Path to your input JSONL file
output_csv = Path(__file__).parent / "sample" / "output.csv"        # Path to your desired output CSV file
sample_size = 5                 # Number of entries to sample
seed = None                      # Random seed for reproducibility (set to an integer for deterministic output)


def sample_jsonl_to_csv(jsonl_path, csv_path, sample_size=20, seed=None):
    """
    Reads a JSONL file, samples a given number of entries at random,
    and writes them to a CSV file.

    Args:
        jsonl_path (str): Path to the input JSONL file.
        csv_path (str): Path to the output CSV file.
        sample_size (int): Number of entries to sample.
        seed (int, optional): Random seed for reproducibility.
    """
    if seed is not None:
        random.seed(seed)

    # Load and parse JSONL entries
    data = []
    with open(jsonl_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                data.append(record)
            except json.JSONDecodeError:
                continue

    # Ensure we have enough entries to sample
    total = len(data)
    if sample_size > total:
        raise ValueError(f"Requested sample size {sample_size} exceeds total entries {total}")

    # Randomly sample the specified number of entries
    sampled = random.sample(data, sample_size)

    # Determine CSV columns from keys of the first sampled entry
    fieldnames = list(sampled[0].keys())

    # Write sampled entries to CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sampled)


if __name__ == '__main__':
    sample_jsonl_to_csv(input_jsonl, output_csv, sample_size, seed)
