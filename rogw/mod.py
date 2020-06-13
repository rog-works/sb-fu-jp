import re
import hashlib
import json
from copy import deepcopy
from typing import List, Dict, Tuple
from dataclasses import dataclass
from rogw.logger import logger
from rogw.modjson import ModJson
from rogw.jsonquery import JsonQuery


@dataclass
class Control:
    code: str
    org_words: str


class Worker:
    def __init__(self, org_text: str, controls: List[Control], context: str) -> None:
        self._org_text = org_text
        self._controls = controls
        self._context = context
        self._post_text = ''

    @property
    def finished(self) -> bool:
        return len(self._post_text) > 0

    @property
    def result(self) -> str:
        return self._post_text

    def prepare(self) -> str:
        pre_text = self._org_text
        for index, control in enumerate(self._controls):
            pattern = re.compile('\\^\\s*' + control.code + ';\\s*' + re.escape(control.org_words) + '\\s*(\\^reset;)?')
            replace = '${' + str(index).zfill(4) + '}' + control.org_words + '${/}'
            pre_text = re.sub(pattern, replace, pre_text)

        return pre_text

    def post(self, trans_text: str):
        post_text = trans_text
        for index, control in enumerate(self._controls):
            pattern = re.compile('\\$\\s*\\{\\s*' + str(index).zfill(4) + '\\s*\\}([^$]+)\\$\\s*\\{/\\}')
            replace = f'^{control.code};\\1 (org: {control.org_words})^reset;'
            post_text = re.sub(pattern, replace, post_text)

        self._post_text = post_text
        self._finish_log()

    def _finish_log(self):
        logger.info(f'finish work. {self._context}')


class Mod:
    _json = ModJson()

    @classmethod
    def load(cls, filepath: str) -> 'Mod':
        return cls(filepath, cls._json.load(filepath))

    def __init__(self, filepath: str, data: dict) -> None:
        self.filepath = filepath
        self._data = data
        self._workers: Dict[str, Worker] = {}
        self.digest = self._calc_digest(data)

    def save(self, filepath: str, data: dict):
        self._json.save(filepath, data)

    @property
    def can_translation(self) -> bool:
        return len([worker for worker in self._workers.values() if worker.finished]) == len(self._workers)

    @property
    def workers(self) -> Dict[str, Worker]:
        return self._workers

    def build_workers(self, json_paths: List[str]) -> Dict[str, Worker]:
        for elem in JsonQuery(self._data).equals(*json_paths):
            org_text, controls = self._parse_text(elem.value)
            context = self._context(elem.full_path)
            self._workers[elem.full_path] = Worker(org_text, controls, context)

        return self._workers

    def translation(self) -> dict:
        result = deepcopy(self._data)
        for elem in JsonQuery(result).equals(*self._workers.keys()):
            elem.value = self._workers[elem.full_path].result

        return result

    def _calc_digest(self, data: dict) -> str:
        return hashlib.md5(json.dumps(data).encode('utf-8')).hexdigest()

    def _context(self, json_path: str) -> str:
        return f'{self.filepath} {json_path}'

    def _parse_text(self, org_text: str) -> Tuple[str, List[Control]]:
        return org_text, self._parse_controls(org_text)

    def _parse_controls(self, org_text: str) -> List[Control]:
        matches = re.finditer(r'\^\s*([a-z]+);([^\^]+)(\^reset;)?', org_text)
        controls = []
        for match in matches:
            code, org_words = match.group(1, 2)
            controls.append(Control(code, org_words))

        return controls
