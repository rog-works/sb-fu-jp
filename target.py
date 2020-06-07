import json
from typing import List


class Target:
    def __init__(self, key: str) -> None:
        config = self._load_config(f'targets/{key}/config.json')
        self.key = key
        self.json_paths = config['json_paths']
        self.files = self._load_files(f'targets/{key}/files.txt')

    def _load_config(self, filepath: str) -> dict:
        with open(filepath) as f:
            return json.load(f)

    def _load_files(self, filepath: str) -> List[str]:
        with open(filepath) as f:
            return [line for line in f.read().split('\n') if line]
