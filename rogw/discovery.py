import re
import subprocess
from typing import List, Dict

from rogw.jsonquery import JsonQuery
from rogw.modjson import ModJson


class Discovery:
    _json = ModJson()

    def search(self, dir: str, pattern: str) -> Dict[str, List[str]]:
        discoveries: Dict[str, List[str]] = {}
        for filepath in self.search_files(dir, pattern):
            data = self._json.load(filepath)
            discover_paths = self.discover(data)
            if discover_paths:
                discoveries[filepath] = discover_paths

        return discoveries

    def search_files(self, dir: str, pattern: str) -> List[str]:
        reg = re.compile(pattern)
        find = ['find', dir, '-type', 'f']
        with subprocess.Popen(find, encoding='utf-8', stdout=subprocess.PIPE) as find_ret:
            filepaths = find_ret.stdout.read().split('\n')
            return [filepath for filepath in filepaths if reg.search(filepath)]

    def discover(self, data: dict) -> List[str]:
        return [elem.full_path for elem in JsonQuery(data, delimiter='/').leaf() if elem.text.find(' ') != -1]
