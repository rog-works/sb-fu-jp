import subprocess
import re
from typing import List, Dict
from jsonquery import JsonQuery
from storage import Storage


class Discovery:
    _storage = Storage()

    def search(self, dir: str, pattern: str) -> Dict[str, List[str]]:
        discoveries: Dict[str, List[str]] = {}
        for filepath in self.search_files(dir, pattern):
            data = self._storage.load(filepath)
            discover_json_paths = self.discover(data)
            if discover_json_paths:
                discoveries[filepath] = discover_json_paths

        return discoveries

    def search_files(self, dir: str, pattern: str) -> List[str]:
        reg = re.compile(pattern)
        find = ['find', dir, '-type', 'f']
        find_ret = subprocess.Popen(find, encoding='utf-8', stdout=subprocess.PIPE)
        filepaths = find_ret.stdout.read().split('\n')
        return [filepath for filepath in filepaths if reg.search(filepath)]

    def discover(self, data: dict) -> List[str]:
        return [elem.full_path for elem in JsonQuery(data, leaf_only=True).all() if elem.text.find(' ') != -1]
