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
    # parser.add_argument(
    #     'csv_path',
    #     type=Path,
    #     help='Path to output the result numeric data.'
    # )
    # parser.add_argument(
    #     'output_img',
    #     type=Path,
    #     help='The path to the image to be saved.'
    # )
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
    plot_and_process_data(get_data(df_sol, df_res))


if __name__ == '__main__':
    main()
