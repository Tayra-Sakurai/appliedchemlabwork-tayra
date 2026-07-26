from ._finder import find_boxes
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Finds the bands"
    )
    parser.add_argument(
        'filepath',
        type=str,
        help='The file path to the image.'
    )
    parser.add_argument(
        '-s',
        '--save',
        help='Where to save the result.',
        type=str,
        default='./runs/detect/predict'
    )
    parser.add_argument(
        'output',
        help='Where to output the result CSV file.',
        type=str
    )
    ns = parser.parse_args()
    find_boxes(ns.filepath, ns.output, ns.save)


if __name__ == '__main__':
    main()
