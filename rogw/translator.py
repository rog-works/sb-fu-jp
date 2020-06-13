from dataclasses import dataclass
from typing import Callable, List, Dict
from urllib import parse
import hashlib
import requests
from rogw.logger import logger
from rogw.cache import Cache


@dataclass
class ApiResponse:
    code: int
    results: Dict[str, str]


class Promise:
    def __init__(self, key: str, text: str, resolver: Callable) -> None:
        self.key = key
        self.text = text
        self._resolver = resolver

    def resolve(self, result: str):
        return self._resolver(result)


class Translator:
    def __init__(self, url: str, cache: Cache, request_size_limit: int) -> None:
        self._url = url
        self._cache = cache
        self._request_size_limit = request_size_limit
        self._promises: List[Promise] = []

    def promise(self, text: str, resolver: Callable):
        digest = self._calc_digest(text)
        if self._cache.exists(digest):
            resolver(self._cache.get(digest)['to'])
            return

        index = len(self._promises)
        key = f't{index}'
        promise = Promise(key, text, resolver)
        self._promises.append(promise)

    def perform(self):
        start = 0
        while start < len(self._promises):
            end = self._collect_promises(start)
            if start == end:
                logger.warning(f'Skip huge text translation. size = {len(self._promises[start].text)}')
                start = start + 1
                continue

            promises = self._promises[start:end]
            res = self._trans_to_jp(promises)
            for promise in promises:
                if promise.key in res.results:
                    digest = self._calc_digest(promise.text)
                    self._cache.set(digest, {'from': promise.text, 'to': res.results[promise.key]})
                    promise.resolve(res.results[promise.key])

            start = end

    def _calc_digest(self, text: str) -> str:
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def _collect_promises(self, start: int) -> int:
        total_text_size = 0
        for index, promise in enumerate(self._promises[start:]):
            text_size = len(parse.quote(promise.text))
            if total_text_size + text_size < self._request_size_limit:
                total_text_size = total_text_size + text_size
            else:
                return start + index

        return len(self._promises)

    def _trans_to_jp(self, promises: List[Promise]) -> ApiResponse:
        query = self._build_query({promise.key: promise.text for promise in promises})
        url = f'{self._url}?{query}'
        return ApiResponse(**self._fetch(url))

    def _build_query(self, targets: dict) -> str:
        return '&'.join([f'{key}={parse.quote(text)}' for key, text in targets.items()])

    def _fetch(self, url: str) -> dict:
        try:
            with requests.get(url, timeout=30, allow_redirects=True) as res:
                return res.json()
        except Exception as e:
            raise Exception('Translation error. error = {e}') from e
