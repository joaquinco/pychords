import argparse
import sys
import os

from pychords.chordino import Chordino


def perform_extraction(file_path):
    """
    Extracts song chords
    """

    ch = Chordino()
    return ch.extract(file_path)


def print_chords(chords):
    for chord in chords:
        print(chord.chord, " - ", chord.timestamp)


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('--nnls-chroma-path')  # , required=True)

    return parser.parse_args(argv)


def main():
    args = parse_arguments(sys.argv[1:])

    if args.nnls_chroma_path:
        os.environ['VAMP_PATH'] = args.nnls_chroma_path
    chords = perform_extraction(args.input_file)

    print_chords(chords)


main()
