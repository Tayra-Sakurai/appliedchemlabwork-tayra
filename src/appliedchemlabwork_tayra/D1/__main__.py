# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from typing import Any
import numpy as np
from ._pattern_match import check_match
import random
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o',
        '--optimize',
        help='Optimizes for minimumn experiment time.',
        action='store_true'
    )
    args = parser.parse_args()
    try:
        v2s: np.ndarray[
            tuple[int],
            np.dtype[np.float64]
        ] = np.arange(700e-3, 1., 1e-2)
        v1s: np.ndarray[
            tuple[int],
            np.dtype[np.float64]
        ] = np.arange(10e-3, 2., 1e-2)
        v3s: np.ndarray[
            tuple[int],
            np.dtype[np.float64]
        ] = np.arange(0, 2.5e-1, 1e-2)
        v4s: np.ndarray[
            tuple[int],
            np.dtype[np.float64]
        ] = np.arange(100e-3, 240e-3, 1e-3)
        l: int = len(v1s) * len(v2s) * len(v3s) * len(v4s)
        plist: list[
            tuple[
                np.float64,
                np.ndarray[tuple[int], np.dtype[Any]]
            ]
        ] = []
        bksps: str = ''
        cnt: int = 0
        for v1 in v1s.flat:
            for v2 in v2s.flat:
                for v3 in v3s.flat:
                    for v4 in v4s.flat:
                        cnt += 1
                        message: str = f'{cnt} / {l}'
                        print(bksps, end='')
                        print(message, end='')
                        bksps = '\b' * len(message)
                        matching, th_cold = check_match(v1, v2, v3, v4)
                        if matching:
                            plist.append((th_cold, np.array([v1, v2, v3, v4])))
        print()
    except KeyboardInterrupt:
        print()
    except Exception as e:
        raise e
    finally:
        if not args.optimize:
            print(random.choice(plist)[1])
        else:
            th_array: np.ndarray[tuple[int], np.dtype[np.float64]] = np.array([
                i[0] for i in plist
            ])
            mindex: np.intp = np.argmin(th_array)
            print(plist[mindex][1])


if __name__ == '__main__':
    main()
