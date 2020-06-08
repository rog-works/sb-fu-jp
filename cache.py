import os
import json


class Cache:
    @classmethod
    def exists(cls, key: str) -> bool:
        return os.path.exists(cls._to_filepath(key))

    @classmethod
    def get(cls, key: str) -> dict:
        with open(cls._to_filepath(key)) as f:
            return json.load(f)

    @classmethod
    def set(cls, key: str, data: dict):
        with open(cls._to_filepath(key), mode='w') as f:
            f.write(json.dumps(data, indent=2))

    @classmethod
    def _to_filepath(cls, key: str) -> str:
        return f'caches/{key}.json'
