import sys
import os
from tqdm import tqdm

class OpenWithTQDM:
    def __init__(self, src, **kwargs):
        self.src = src
        self.kwargs = kwargs
        self.fp = None
        size = os.path.getsize(src)
        self.pbar = tqdm(total=size)
        self.encoding = kwargs["encoding"] if "encoding" in kwargs else sys.getdefaultencoding()

    def __init(self):
        if self.fp is None:
            # overwrite newline arg
            if "newline" in self.kwargs:
                print("warning: \"newline\" arg does not work.")
            self.kwargs["newline"] = ""
            self.fp = open(self.src, **self.kwargs)

    def __del__(self):
        if self.fp is not None:
            self.fp.close()
        self.pbar.clear()
        self.pbar.close()

    def __iter__(self):
        self.__init()
        return self

    def __next__(self):
        l = self.fp.__next__()
        self.pbar.update(len(l.encode(self.encoding)))
        return l.strip()

    def __enter__(self):
        self.__init()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()
