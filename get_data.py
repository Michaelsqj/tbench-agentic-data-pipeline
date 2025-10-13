#!/Users/qijia/Documents/miniforge3/envs/terminal_agent/bin/python
import numpy as np
import json
import os
from pathlib import Path


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description="Load and display dataset information.")
    parser.add_argument("-i", type=int, default=0, help="Index of the datapoint to display")
    args = parser.parse_args()
    # Example usage
    file = Path(__file__).parent / "state" / "dataset.json"

    with open(file, "r") as f:
        data = json.load(f)
    print(f"Dataset total length: {len(data)}")
    
    print(f"Displaying datapoint at index {args.i}:")
    print(json.dumps(data[args.i], indent=2))