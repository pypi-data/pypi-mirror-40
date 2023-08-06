from smartreplace import sreplace
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('regex')
parser.add_argument('replacer')
parser.add_argument('file_query')
args = parser.parse_args()


def run():
    sreplace(
        regex=args.regex,
        replacer=args.replacer,
        file_query=args.file_query
    )
