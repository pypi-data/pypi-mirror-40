from smartreplace import sreplace
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('regex', help='regex to find needle')
parser.add_argument('replacer', help='what to replace needle with')
parser.add_argument(
    'file_query', help='which files to look in, example: "*.py"')
args = parser.parse_args()


def run():
    sreplace(
        regex=args.regex,
        replacer=args.replacer,
        file_query=args.file_query
    )
