import argparse
from lz78 import handle_compression, handle_decompression


def setup_argument_parser():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    group = required.add_mutually_exclusive_group(required=True)

    group.add_argument("-c", "--compress", type=str, help="file to compress")
    group.add_argument("-x", "--decompress", type=str,
                       help="file to decompress")

    parser.add_argument("-o", "--output", type=str, help="output file")

    return parser


def main():
    parser = setup_argument_parser()
    args = parser.parse_args()

    if (args.compress):
        handle_compression(args)
    else:
        handle_decompression(args)


if __name__ == "__main__":
    main()
