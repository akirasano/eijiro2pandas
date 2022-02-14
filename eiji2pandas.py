import sys
import os
import re
import pathlib
import pandas as pd

from openwithtqdm import OpenWithTQDM


def extract(l: str):
    word, content = l.split(" : ")
    word = word.replace(r"■", "")

    mr = re.search(r"\{(.+?)\}", word)
    if mr is not None:
        word = word.replace(mr.group(0), "")
        part = mr.group(1)
    else:
        part = ""

    return word, part, content


if __name__ == "__main__":
    src = "EIJIRO-1448.TXT" if len(sys.argv) == 1 else sys.argv[0]
    base = os.path.splitext(os.path.basename(src))[0]

    if pathlib.Path(base + ".pkl").exists():
        df = pd.read_pickle(base + ".pkl")
    else:
        words = []
        parts = []
        contents = []

        with OpenWithTQDM(src, encoding="cp932") as fp:
            for l in fp:
                w, p, c = extract(l)
                words.append(w)
                parts.append(p)
                contents.append(c)

        df = pd.DataFrame(
            data={"word": words, "part": parts, "contents": contents})
        df.to_pickle(base + ".pkl")
        df["word"].to_csv(base + ".csv")
