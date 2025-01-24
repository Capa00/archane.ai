from abc import ABC, abstractmethod


class Module(ABC):
    @abstractmethod
    def observe_environment(self, *args, **kwargs):
        ...

    @abstractmethod
    def read_state(self, *args, **kwargs):
        ...

    @abstractmethod
    def write_state(self, *args, **kwargs):
        ...

    @abstractmethod
    def run(self, *args, **kwargs):
        ...

