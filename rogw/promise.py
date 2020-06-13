from abc import ABCMeta, abstractmethod


class IPromise(metaclass=ABCMeta):
    @property
    @abstractmethod
    def done(self) -> bool:
        assert False, 'Not implemented method'

    @property
    @abstractmethod
    def result(self) -> str:
        assert False, 'Not implemented method'
