import pandas
import argparse
from pathlib import Path
from ._loader import *


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Outputs a data table and graphs of the result of A3 experiment."
    )
    parser.add_argument(
        'input_sol',
        type=Path,
        help='The path to the file where the solution data are stored.'
    )
    parser.add_argument(
        'input_res',
        type=Path,
        help='The path to the file where the time data is stored.'
    )
    parser.add_argument(
        'output_path1',
        type=Path,
        help='The path to the file to save result. Mainly the viscosity data.'
    )
    parser.add_argument(
        'output_path2',
        type=Path,
        help='The molecular weight and other data output path.'
    )
    ns = parser.parse_args()
    df_sol = pandas.read_csv(
        ns.input_sol,
        encoding='utf_8_sig',
        header=0
    )
    df_res = pandas.read_csv(
        ns.input_res,
        encoding='utf_8_sig',
        header=0
    )
    plot_and_process_data(get_data(df_sol, df_res), ns.output_path1, ns.output_path2)


if __name__ == '__main__':
    main()
