import argparse
import os
from pathlib import Path
import jack_compiler

def main():
    parser = argparse.ArgumentParser(description="Process a file path.")
    parser.add_argument("path", type=str, help="The path to the file")
    parser.add_argument("-o", "--output", type=str, help="The output file path")

    args = parser.parse_args()
    input_path = Path(os.path.abspath(args.path))

    output_path = input_path.parent / f"{input_path.stem}_output" if args.output is None else args.output

    print(f"Args: input path: {input_path}, output path: {output_path}")

    jack_compiler.compile_jack_code(str(input_path), output_path)


if __name__ == '__main__':
    main()
