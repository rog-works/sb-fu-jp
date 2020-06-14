from copy import deepcopy
import hashlib
import json
from typing import Dict

from rogw.jsonquery import JsonQuery
from rogw.modjson import ModJson
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
        return 0 < len(self.promises) == len([promise for promise in self.promises.values() if promise.done])

    def translation(self) -> dict:
        result = deepcopy(self.data)
        for elem in JsonQuery(result, delimiter='/').equals(*self.promises.keys()):
            elem.value = self.promises[elem.full_path].result

        return result

    def save(self, filepath: str, data: dict):
        self._json.save(filepath, data)
