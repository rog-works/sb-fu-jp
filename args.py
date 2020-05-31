from typing import List, Tuple


class Args:
    def __init__(self, argv: List[str]) -> None:
        dest, keys, files = self.parse(argv)
        self.dest = dest
        self.keys = keys
        self.files = files

    def parse(self, argv: List[str]) -> Tuple[str, List[str], List[str]]:
        option = ''
        dest = ''
        keys = []
        files = []
        for value in argv[1:]:
            if value.startswith('--'):
                option = value[2:]
                continue

            if len(value) == 0:
                continue

            if option == 'files':
                files = (value if not value.endswith(',') else value[:-1]).split(',')
            elif option == 'keys':
                keys = (value if not value.endswith(',') else value[:-1]).split(',')
            elif option == 'dest':
                dest = value

            option = ''

        return dest, keys, files
