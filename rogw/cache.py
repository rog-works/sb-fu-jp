import os
import json


class Cache:
    def __init__(self, dir: str) -> None:
        self._dir = dir

    def exists(self, key: str) -> bool:
        return os.path.exists(self._to_filepath(key))

    def get(self, key: str) -> dict:
        with open(self._to_filepath(key)) as f:
            return json.load(f)

    def set(self, key: str, data: dict):
        with open(self._to_filepath(key), mode='w') as f:
            f.write(json.dumps(data, indent=2))

    def _to_filepath(self, key: str) -> str:
        return f'{self._dir}/{key}.json'
