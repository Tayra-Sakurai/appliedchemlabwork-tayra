from ._finder import find_boxes
from ._plot_module import plot_dna
import argparse
import pandas
import matplotlib.style


def main():
    parser = argparse.ArgumentParser(
        description="Finds or plots the bands."
    )
    subcommands = parser.add_subparsers(
        title='command',
        description='Selects the actions.',
        help='The action.',
        required=True
    )
    find = subcommands.add_parser(
        'find',
        help='Finds the bands from image.',
        description='Finds the bands from image.'
    )
    plot = subcommands.add_parser(
        'plot',
        description='Plots the band locations to the length of the DNA.',
        help='Plots the location to length.'
    )
    find.add_argument(
        'filepath',
        type=str,
        help='The file path to the image.'
    )
    find.add_argument(
        '-s',
        '--save',
        help='Where to save the result.',
        type=str,
        default='./runs/detect/predict'
    )
    find.add_argument(
        'output',
        help='Where to output the result CSV file.',
        type=str
    )
    plot.add_argument(
        'datafilepath',
        help='The file path to the CSV data file.',
        type=str
    )
    plot.add_argument(
        '-t',
        '--style',
        choices=matplotlib.style.available,
        type=str,
        default='default',
        help='Plot style'
    )
    ns = parser.parse_args()
    if 'filepath' in ns:
        find_boxes(ns.filepath, ns.output, ns.save)
    else:
        result = plot_dna(
            pandas.read_csv(
                ns.datafilepath,
                encoding='utf_8_sig',
                header=0,
                index_col=False
            ),
            ns.style
        )
        print('Resuls:')
        print(result[0])
        print('Errors:')
        print(result[1])


if __name__ == '__main__':
    main()
