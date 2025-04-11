import argparse
import os
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Process a file path.")
    parser.add_argument("path", type=str, help="The path to the file")
    parser.add_argument("-o", "--output", type=str, help="The output file path")

    args = parser.parse_args()
    full_path = os.path.abspath(args.path)
    output_path = Path(full_path).parent

    print(f"Args: {full_path}")

if __name__ == '__main__':
    main()