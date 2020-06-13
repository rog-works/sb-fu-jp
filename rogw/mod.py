import json
import hashlib
from copy import deepcopy
from typing import Dict
from rogw.modjson import ModJson
from rogw.jsonquery import JsonQuery
from rogw.promise import IPromise


class Mod:
    _json = ModJson()

    @classmethod
    def load(cls, filepath: str) -> 'Mod':
        return cls(filepath, cls._json.load(filepath))

    def __init__(self, filepath: str, data: dict) -> None:
        self.filepath = filepath
        self.data = data
        self.digest = self._calc_digest(data)
        self.promises: Dict[str, IPromise] = {}

    def _calc_digest(self, data: dict) -> str:
        return hashlib.md5(json.dumps(data).encode('utf-8')).hexdigest()

    @property
    def can_translation(self) -> bool:
        return len([promise for promise in self.promises.values() if promise.done]) == len(self.promises)

    def translation(self) -> dict:
        result = deepcopy(self.data)
        for elem in JsonQuery(result).equals(*self.promises.keys()):
            elem.value = self.promises[elem.full_path].result

        return result

    def save(self, filepath: str, data: dict):
        self._json.save(filepath, data)
