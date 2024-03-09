from abc import ABC, abstractmethod

class Contract(ABC):

    @abstractmethod
    def check(self, x)-> bool:
        ...
    
    @abstractmethod
    def generate(self, fuel) -> any:
        ...
    
    def symbolic(self, name: str | None = None):
        raise NotImplementedError(f"Symbolic representation not implemented for {self}")
