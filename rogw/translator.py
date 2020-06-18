from dataclasses import dataclass
import hashlib
import requests
from typing import Dict, List, Tuple
from urllib import parse

from rogw.cache import Cache
from rogw.logger import report
from rogw.promise import IPromise
from rogw.worker import IWorker


@dataclass
class ApiResponse:
    code: int
    results: Dict[str, str]


class Promise(IPromise):
    def __init__(self, key: str, worker: IWorker) -> None:
        self.key = key
        self._worker = worker
        self._result = ''

    @property
    def done(self) -> bool:
        return len(self._result) > 0

    @property
    def text(self) -> str:
        return self._worker.text

    @property
    def result(self) -> str:
        return self._result

    @result.setter
    def result(self, value: str):
        self._result = self._worker.run(value)


class Translator:
    def __init__(self, url: str, cache: Cache, request_size_limit: int) -> None:
        self._url = url
        self._cache = cache
        self._request_size_limit = request_size_limit
        self._promises: List[Promise] = []

    def enqueue(self, worker: IWorker) -> IPromise:
        digest = self._calc_digest(worker.text)
        if self._cache.exists(digest):
            promise = Promise('', worker)
            promise.result = self._cache.get(digest)['to']
            return promise

        key = f't{len(self._promises)}'
        promise = Promise(key, worker)
        self._promises.append(promise)
        return promise

    def perform(self):
        start = 0
        while start < len(self._promises):
            end = self._collect_promises(start)
            if start == end:
                report.warning(f'Skip huge text translation. size = {len(self._promises[start].text)}, text = {self._promises[start].text}')
                start = start + 1
                continue

            promises = self._promises[start:end]
            res = self._trans_to_jp(promises)
            for promise in promises:
                if promise.key in res.results:
                    digest = self._calc_digest(promise.text)
                    self._cache.set(digest, {'from': promise.text, 'to': res.results[promise.key]})
                    promise.result = res.results[promise.key]

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
            with requests.get(url, timeout=60, allow_redirects=True) as res:
                succeeded, body = self._parse_body(res)
                if succeeded:
                    return body

                error_message = f'Failed request. status = {res.status_code}, response = {res.text}'
                report.error(f'{error_message}, url = {url}')
                raise Exception(error_message)
        except Exception as e:
            raise Exception(f'Fetch error. error = [{type(e)}] {e}') from e

    def _parse_body(self, res: requests.Response) -> Tuple[bool, dict]:
        if res.status_code < 200 or res.status_code >= 300:
            return False, {}

        if res.headers['content-type'].find('application/json') == -1:
            return False, {}

        body = res.json()
        return len(body['result']) > 0, body
