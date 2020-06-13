from abc import ABCMeta, abstractmethod


class IWorker(metaclass=ABCMeta):
    @property
    @abstractmethod
    def text(self) -> str:
        assert False, 'Not implemented method'

    @abstractmethod
    def run(self, trans_text: str) -> str:
        assert False, 'Not implemented method'
