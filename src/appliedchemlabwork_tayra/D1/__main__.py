from typing import Any
import numpy as np
from ._pattern_match import check_match
import random


def main():
    v2s = np.arange(700e-3, 1., 1e-2)
    v1s = np.arange(10e-3, 2., 1e-2)
    v3s = np.arange(0, 2.5e-1, 1e-3)
    v4s = np.arange(0, 240e-3, 1e-3)
    plist: list[np.ndarray[tuple[int], np.dtype[Any]]] = []
    for v1 in np.nditer(v1s):
        for v2 in np.nditer(v2s):
            for v3 in np.nditer(v3s):
                for v4 in np.nditer(v4s):
                    if check_match(v1, v2, v3, v4):
                        plist.append(np.array([v1, v2, v3, v4]))
    print(random.choice(plist))


if __name__ == '__main__':
    main()
