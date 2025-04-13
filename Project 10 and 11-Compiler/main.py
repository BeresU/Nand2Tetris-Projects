import argparse
import os
from pathlib import Path
import jack_analyzer

def main():
    parser = argparse.ArgumentParser(description="Process a file path.")
    parser.add_argument("path", type=str, help="The path to the file")
    parser.add_argument("-o", "--output", type=str, help="The output file path")

    args = parser.parse_args()
    input_path = os.path.abspath(args.path)
    output_path = Path(input_path).parent if args.output is None else args.output

    print(f"Args: input path: {input_path}, output path: {output_path}")

    jack_analyzer.analyze(input_path, output_path)

if __name__ == '__main__':
    main()