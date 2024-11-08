import argparse
import sys
import pathlib

from predict import predict
import tools

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This find code clone in python code")
    # parser.add_argument("-t", "--threshold", type=float, default=0.9) # Can use it if needed

    parser.add_argument(
        "-o", "--output", help="Output path, if not set output to stdout", type=str
    )
    parser.add_argument(
        "-m", "--model", help="Model path", default="src\\model\\model.m", type=str
    )
    parser.add_argument(
        "-k", "--top_k", help="Num of potential clones", default=20, type=int
    )
    parser.add_argument("target", help="Target code file name", type=str)
    parser.add_argument("sources", help="Source codes dir path", type=str)
    args = vars(parser.parse_args())

    # threshold = args["threshold"]
    sources_path = pathlib.Path(args["sources"])
    target = args["target"]
    model_path = pathlib.Path(args["model"])
    top_k = args["top_k"]
    outputPath = sys.stdout if args["output"] is None else open(args["output"], "w+")

    sources = tools.read_from_dir(sources_path)
    pred, clones = predict(sources, [target], model_path, top_k)[target]

    if pred:
        print("clone")
    else:
        print("unique")
    print("potential clone of:\n", ", ".join(clones))

    # << python src\cli.py 1024.py yandex_clear
    # >> unique
    # >> potential clone of:
    # >> 1011.py, 1186.py, 1417.py, 1458.py, 715.py, 849.py, 872.py, 915.py, 0.py, 1.py, 10.py, 100.py, 1000.py, 1001.py, 1002.py, 1003.py, 1004.py, 1005.py, 1006.py, 1007.py

    # << python src\cli.py 777.py yandex_plag
    # >> clone
    # >> potential clone of:
    # >> 1252.py, 188.py, 539.py, 653.py, 673.py, 47.py, 49.py, 603.py, 793.py, 1418.py, 144.py, 411.py, 694.py, 1311.py, 771.py, 836.py, 1078.py, 1248.py, 1250.py, 1430.py
