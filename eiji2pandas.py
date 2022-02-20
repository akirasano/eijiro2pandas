import argparse
import pickle
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd

from openwithtqdm import OpenWithTQDM


def extract(line: str) -> Tuple[str, str, str]:
    word, content = line.split(" : ")
    word = word.replace(r"■", "")

    mr = re.search(r"\{(.+?)\}", word)
    if mr is not None:
        word = word.replace(mr.group(0), "").strip()
        part = mr.group(1)
    else:
        part = ""

    return word, part, content


if __name__ == "__main__":
    parser = argparse.ArgumentParser("EIJIRO text converter")
    parser.add_argument("-i", "--input", help="INTPUT", default="EIJIRO-1448.TXT")
    parser.add_argument("-o", "--output", help="OUTPUT", default="EIJIRO-1448.pkl")
    parser.add_argument("--dict", help="Write as python dict pkl", action="store_true")
    parser.add_argument("-y", help="Overwrite output file", action="store_true")

    args = parser.parse_args()

    src = Path(args.input)
    dst = Path(args.output)

    if not src.exists():
        print(f"Error: input file {src} is not found.")
        sys.exit(1)

    if not args.y and dst.exists():
        s = input(f"{dst} already exists. Overwrite? [y/N] ")
        if s.lower().strip() != "y":
            print("Not overwriting.")
            sys.exit(0)

    words = []
    parts = []
    contents = []

    if not args.dict:
        with OpenWithTQDM(src, encoding="cp932") as fp:
            for line in fp:
                w, p, c = extract(line)
                words.append(w)
                parts.append(p)
                contents.append(c)

        df = pd.DataFrame(data={"word": words, "part": parts, "contents": contents})
        df.to_pickle(dst)
        print(f"Saved {dst} as pandas datapframe.")

    else:
        wd: Dict[str, List[Tuple[str, str]]] = {}
        with OpenWithTQDM(src, encoding="cp932") as fp:
            for line in fp:
                w, p, c = extract(line)
                if w in wd:
                    wd[w].append((p, c))
                else:
                    wd[w] = [(p, c)]

        with open(dst, "wb") as fp:
            pickle.dump(wd, fp, protocol=pickle.HIGHEST_PROTOCOL)

        print(f"Saved {dst} as python dict pickle file.")
