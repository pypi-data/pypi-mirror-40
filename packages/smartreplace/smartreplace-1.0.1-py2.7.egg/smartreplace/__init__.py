import fnmatch
import os
import re
import difflib


def user_input(text):
    methods = globals()['__builtins__'].__dict__
    return methods['input'](text) if 'input' in methods else raw_input(text)  # NOQA


def _unidiff_output(expected, actual):
    expected = expected.splitlines(1)
    actual = actual.splitlines(1)

    diff = difflib.unified_diff(expected, actual)

    return ''.join(diff)


def sreplace(regex, replacer, file_query='*.py'):
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, file_query):
            fname = os.path.join(root, filename)
            contents = open(fname).read()

            new_contents = re.sub(
                regex,
                replacer,
                contents
            )

            diff = _unidiff_output(contents, new_contents)

            if not diff:
                continue

            print(diff)

            ans = user_input(  # NOQA
                '[{}] Write? (y/n)'
                .format(fname)
            )

            if ans.lower() == 'y':
                open(fname, 'w+').write(new_contents)
                print('[{}] File written.'.format(fname))
