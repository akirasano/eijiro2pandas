import sys
import pathlib
import pandas as pd


if __name__ == "__main__":
    query = sys.argv[1:]

    src = "EIJIRO-1448.pkl"

    if pathlib.Path(src).exists():
        df = pd.read_pickle(src)
    else:
        print(f"Error: {src} is not found.")
        sys.exit(1)

    qstr = " & ".join([f"word.str.contains('{q}', regex=True)" for q in query])
    print(qstr)
    print(df.query(qstr, engine='python'))
