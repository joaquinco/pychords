import argparse
import sys
import os

from pychords.chordino import Chordino


def perform_extraction(args):
    """
    Extracts song chords
    """

    ch = Chordino(
        use_nnls=args.use_nnls,
        use_hart_notation=args.use_hart_notation,
        roll_on=args.roll_on,
        local_tunning=args.local_tunning,
        spectral_whitening=args.whitening,
        spectral_shape=args.shape,
        boost_n_likelihood=args.boost_n,
    )
    return ch.extract(args.input_file)


def print_chords(chords):
    for chord in chords:
        print(chord.chord, " - ", chord.timestamp)


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('--nnls-chroma-path')
    parser.add_argument(
        '--use-nnls', action='store_true', default=False)
    parser.add_argument(
        '--use-hart-notation', action='store_true', default=False)
    parser.add_argument(
        '--local-tunning', action='store_true', default=False)
    parser.add_argument(
        '--roll-on', type=float, default=1.0, help='Between 1 0 and 5')
    parser.add_argument(
        '--whitening', type=float, default=1.0, help='Between 0 and 1')
    parser.add_argument(
        '--shape', type=float, default=0.7, help='Between 0.5 and 0.9')
    parser.add_argument(
        '--boost-n', type=float, default=0.1, help='Between 0 and 1')

    return parser.parse_args(argv)


def main():
    args = parse_arguments(sys.argv[1:])

    if args.nnls_chroma_path:
        os.environ['VAMP_PATH'] = args.nnls_chroma_path
    chords = perform_extraction(args)

    print_chords(chords)


main()
