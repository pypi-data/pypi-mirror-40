from abc import abstractmethod, ABCMeta

from ConfigReader.ConfigReader import ConfigReader


class Step(ConfigReader):
    __metaclass__ = ABCMeta

    @abstractmethod
    def perform(self):
        pass  # pragma: no cover
