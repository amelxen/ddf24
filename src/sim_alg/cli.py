import argparse
import sys

import os
def dummy_find_clones(directory: str):
    res = {}
    for root, dir, files in os.walk(directory):
        res[root] = list(files)
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This find code clone in python code")
    # parser.add_argument("-t", "--threshold", type=float, default=0.9) # Can use it if needed
    
    parser.add_argument("-o", "--output", help="Output path, if not set output to stdout", type=str)
    parser.add_argument("directory")
    args = vars(parser.parse_args())

    # threshold = args["threshold"]
    directory = args["directory"]
    outputPath = sys.stdout if args["output"] is None else open(args["output"], "w+")
    
    res = dummy_find_clones(directory)
    for next_file, clones in res.items():
        if len(clones) == 0:
            print(f"{next_file} - is unique", file=outputPath, flush=True)
        else:
            print(f"{next_file} - potential clone of: \n  {"\n  ".join(clones)}", file=outputPath, flush=True)
