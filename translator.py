from dataclasses import dataclass
from typing import List, Dict
from urllib import parse
import requests
from logger import logger


class Promise:
    def __init__(self, key: str, text: str) -> None:
        self.key = key
        self.text = text
        self.result = text

    def resolve(self):
        return self.result


@dataclass
class ApiResponse:
    code: int
    results: Dict[str, str]


class Translator:
    def __init__(self, url: str, together_limit_size: int) -> None:
        self._url = url
        self._together_limit_size = together_limit_size
        self._promises: List[Promise] = []

    def future(self, text: str) -> Promise:
        index = len(self._promises)
        key = f't{index}'
        promise = Promise(key, text)
        self._promises.append(promise)
        return promise

    def perform(self):
        start = 0
        while start < len(self._promises):
            end = self.collect_promises(start)
            promises = self._promises[start:end]
            res = self.trans_to_jp(promises)
            for promise in promises:
                if promise.key in res.results:
                    promise.result = res.results[promise.key]

            start = end

    def collect_promises(self, start: int) -> int:
        total_text_size = 0
        for index, promise in enumerate(self._promises[start:]):
            text_size = len(parse.quote(promise.text))
            if total_text_size + text_size < self._together_limit_size:
                total_text_size = total_text_size + text_size
            else:
                return start + index

        return len(self._promises)

    def trans_to_jp(self, promises: List[Promise]) -> ApiResponse:
        query = self.build_query({promise.key: promise.text for promise in promises})
        url = f'{self._url}?{query}'
        return ApiResponse(**self.fetch(url))

    def build_query(self, targets: dict) -> str:
        return '&'.join([f'{key}={parse.quote(text)}' for key, text in targets.items()])

    def fetch(self, url: str) -> dict:
        try:
            with requests.get(url, allow_redirects=True) as res:
                return res.json()
        except Exception as e:
            raise Exception('Translation error') from e
