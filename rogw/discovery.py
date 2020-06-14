import re
import subprocess
from typing import List, Dict

from rogw.jsonquery import JsonQuery
from rogw.modjson import ModJson
from rogw.logger import logger, report


class Discovery:
    _json = ModJson()

    def search(self, dir: str, pattern: str) -> Dict[str, List[str]]:
        discoveries: Dict[str, List[str]] = {}
        for filepath in self._search_files(dir, pattern):
            discover_paths = self._discover(filepath)
            if discover_paths:
                discoveries[filepath] = discover_paths

        return discoveries

    def _search_files(self, dir: str, pattern: str) -> List[str]:
        reg = re.compile(pattern)
        find = ['find', dir, '-type', 'f']
        with subprocess.Popen(find, encoding='utf-8', stdout=subprocess.PIPE) as find_ret:
            filepaths = find_ret.stdout.read().split('\n')
            return [filepath for filepath in filepaths if reg.search(filepath)]

    def _discover(self, filepath: str) -> List[str]:
        try:
            data = self._json.load(filepath)
            return [elem.full_path for elem in JsonQuery(data, delimiter='/').leaf() if elem.text.find(' ') != -1]
        except Exception as e:
            error_message = f'filepath = {filepath} error = [{type(e)}] {e}'
            logger.error(error_message)
            report.error(error_message)
            return []
