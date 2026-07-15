# SPDX-FileCopyrightText: 2026-present Tayra Sakurai <tayra_sakurai@icloud.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
import argparse
from ._calc_conc import calc_concentration
from pathlib import Path
import pandas


def main() -> None:
    parser = argparse.ArgumentParser(
        prog='AppliedChamLabWork_tayra.D2',
        description='Analyzer for the D2 experiment.'
    )
    parser.add_argument(
        'datafilepath',
        type=Path,
        help='The file path to the data CSV file.'
    )
    parser.add_argument(
        'epsilonpath',
        type=Path,
        help='The file path to the data CSV file for the molar absorption coefficients.'
    )
    parser.add_argument(
        '-l',
        '--length',
        type=float,
        default=1.0e-2,
        help='The optical length of the cell.'
    )
    parser.add_argument(
        '-e',
        '--encoding',
        type=str,
        help='The encoding of the data files.',
        default='utf_8_sig'
    )
    args = parser.parse_args()
    data = pandas.read_csv(
        args.datafilepath,
        encoding=args.encoding,
        header=0,
        index_col=False)
    epsilon = pandas.read_csv(
        args.epsilonpath,
        encoding=args.encoding,
        header=0,
        index_col=False)
    df = calc_concentration(
        data,
        epsilon,
        args.length
    )
    print(df)
    print()
    print(df.to_latex())


if __name__ == '__main__':
    main()
