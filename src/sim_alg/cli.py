import argparse
import sys

class dummy:
    def process(f):
        if(len(f) < 5):
            return [f, f]
        return []

def process(next_file: str, d: dummy):
    res = dummy.process(next_file)
    if len(res) == 0:
        print(f"{next_file} - is unique", file=outputPath, flush=True)
    else:
        print(f"{next_file} - potential clone of: \n  {"\n  ".join(res)}", file=outputPath, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This find code clone in python code")
    # parser.add_argument("-t", "--threshold", type=float, default=0.9) # Can use it if needed
    
    parser.add_argument("-b", "--base", help="Files for comparison (these files will not be selected for search)", type=str, nargs="+")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--compare", help="Files for comparison", type=str, nargs="+")
    group.add_argument("-i", "--interactive", help="Interactive mode, each new file is compared with all previous ones and added to the database", action=argparse.BooleanOptionalAction)
    parser.add_argument("-o", "--output", help="Output path, if not set output to stdout", type=str)
    args = vars(parser.parse_args())

    base = [] if args["base"] is None else args["base"]
    compare = args["compare"]
    # threshold = args["threshold"]
    interactive = False if args["interactive"] is None or args["interactive"] == False else True
    outputPath = sys.stdout if args["output"] is None else open(args["output"], "w+")
    
    d = dummy()

    for next_file in base:
        d.process(next_file)
    
    if interactive:
        while(True):
            next_file = input("Enter next filepath or exit: ")
            if(next_file == "exit"):
                break
            process(next_file, d)
    else:
        for next_file in compare:
            process(next_file, d)