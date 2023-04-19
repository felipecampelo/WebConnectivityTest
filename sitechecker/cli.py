import argparse

def read_user_cli_args():

    parser = argparse.ArgumentParser(
        prog="sitechecker", description="Teste a disponibilidade de uma URL"
    )

    parser.add_argument(
        "-u",
        "--urls",
        metavar="URLs",
        nargs="+",
        type=str,
        default=[],
        help="Insira um ou mais URLs"
    )

    parser.add_argument("--file", type=argparse.FileType('r'))

    return parser.parse_args()