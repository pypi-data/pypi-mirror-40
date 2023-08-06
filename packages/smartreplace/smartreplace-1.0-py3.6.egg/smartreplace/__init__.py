import fnmatch
import os
import re
import difflib


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

            matches = re.findall(regex, contents)

            for match in matches:
                new_contents = re.sub(
                    regex,
                    replacer,
                    contents
                )

                print(_unidiff_output(contents, new_contents))

                ans = raw_input(  # NOQA
                    '[{}] Replace {} with {} ? (y/n)'
                    .format(fname, match, replacer)
                )

                if ans.lower() == 'y':
                    open(fname, 'w+').write(new_contents)
                    print('[{}] File written.'.format(fname))
