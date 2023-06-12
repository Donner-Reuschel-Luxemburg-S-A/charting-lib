from abc import ABC, abstractmethod


class Chart(ABC):

    @abstractmethod
    def apply_formatting(self):
        pass

    @abstractmethod
    def apply_transformation(self):
        pass

    @abstractmethod
    def plot(self, directory: str = ""):
        pass
