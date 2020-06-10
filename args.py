from typing import List, Tuple


class Args:
    def __init__(self, argv: List[str]) -> None:
        targets, discover, force = self.parse(argv)
        self.targets = targets
        self.discover = discover
        self.force = force

    def parse(self, argv: List[str]) -> Tuple[List[str], bool, bool]:
        targets = []
        discover = False
        force = False
        index = 0
        while(index < len(argv)):
            if index == 0 or not argv[index].startswith('--'):
                index = index + 1
                continue

            option = argv[index][2:]
            if option == 'target':
                index = index + 1
                targets.append(argv[index])
            elif option == 'discover':
                discover = True
            elif option == 'force':
                force = True

            index = index + 1

        return targets, discover, force
