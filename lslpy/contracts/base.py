from abc import ABC, abstractmethod

class Contract(ABC):

    @abstractmethod
    def check(self, x)-> bool:
        ...
    
    @abstractmethod
    def generate(self, fuel) -> any:
        ...
