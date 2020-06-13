import json
import os


class Cache:
    def __init__(self, dir: str) -> None:
        self._dir = dir

    def exists(self, key: str) -> bool:
        return os.path.exists(self._to_filepath(key))

    def get(self, key: str) -> dict:
        with open(self._to_filepath(key)) as f:
            return json.load(f)

    def set(self, key: str, data: dict):
        filepath = self._to_filepath(key)
        self._try_mkdir(filepath)
        with open(filepath, mode='w') as f:
            f.write(json.dumps(data, indent=2))

    def _to_filepath(self, key: str) -> str:
        return os.path.join(self._dir, key[:2], f'{key}.json')

    def _try_mkdir(self, filepath: str):
        dir = os.path.dirname(filepath)
        if not os.path.exists(dir):
            os.mkdir(dir)
