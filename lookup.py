import argparse
import sys
from pathlib import Path

import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Look up a word in the dictionary.")
    parser.add_argument("-i", "--input", help="INTPUT", default="EIJIRO-1448.pkl")
    parser.add_argument("query", help="search queries (regex)", nargs="+")
    parser.add_argument("-o", "--output", help="Output (csv)")

    args = parser.parse_args()

    src = Path(args.input)
    query = args.query

    if not src.exists():
        print(f"Error: {src} is not found.")
        sys.exit(1)

    df = pd.read_pickle(src)
    qstr = " & ".join([f"word.str.contains('{q}', regex=True)" for q in query])
    print(f"Query str: {qstr}")
    r: pd.DataFrame = df.query(qstr, engine="python")
    if args.output:
        r.to_csv(args.output)
    else:
        print(r)
