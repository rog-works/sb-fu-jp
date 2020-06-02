import re
from copy import deepcopy
from typing import List, Dict, Tuple
from dataclasses import dataclass
from logger import logger


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
            pattern = re.compile('\\^' + control.code + ';([^^]+)\\^reset;')
            replace = '${' + str(index).zfill(4) + '}' + control.org_words + '${/}'
            pre_text = re.sub(pattern, replace, pre_text)

        return pre_text

    def post(self, trans_text: str):
        post_text = trans_text
        for index, control in enumerate(self._controls):
            pattern = re.compile('\\$\\s*\\{' + str(index).zfill(4) + '\\}\\s*([^$]+)\\s*\\$\\s*\\{/\\}')
            replace = f'^{control.code};\\1 (org: {control.org_words})^reset;'
            post_text = re.sub(pattern, replace, post_text)

        self._post_text = post_text
        self._finish_log()

    def _finish_log(self):
        logger.info(self._context)


class Mod:
    def __init__(self, filepath: str, data: dict) -> None:
        self.filepath = filepath
        self._data = data
        self._workers: Dict[str, Worker] = {}

    @property
    def has_translate(self) -> bool:
        return len([worker for worker in self._workers.values() if worker.finished]) > 0

    def works(self, json_paths: List[str]) -> List[Worker]:
        for json_path in json_paths:
            if self._path_exists(self._data, json_path):
                org_text, controls = self._parse_row(self._data, json_path)
                context = self._context(json_path)
                self._workers[json_path] = Worker(org_text, controls, context)

        return [worker for worker in self._workers.values()]

    def translated(self) -> dict:
        result = deepcopy(self._data)
        for json_path, worker in self._workers.items():
            self._infuse(result, json_path, worker.result)

        return result

    def _context(self, json_path: str) -> str:
        return f'{self.filepath} {json_path}'

    def _parse_row(self, data: dict, json_path: str) -> Tuple[str, List[Control]]:
        org_text = self._extract(data, json_path)
        return org_text, self._parse_controls(org_text)

    def _parse_controls(self, org_text: str) -> List[Control]:
        matches = re.finditer(r'\^([a-z]+);([^\^]+)\^reset;', org_text)
        controls = []
        for match in matches:
            code, org_words = match.group(1, 2)
            controls.append(Control(code, org_words))

        return controls

    def _path_exists(self, data: dict, json_path: str) -> bool:
        return json_path in self._data

    def _extract(self, data: dict, json_path: str) -> str:
        return data[json_path]

    def _infuse(self, data: dict, json_path: str, post_text: str):
        data[json_path] = post_text
