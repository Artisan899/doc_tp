from abc import ABC, abstractmethod

class BaseSpecification(ABC):
    @abstractmethod
    def apply_filter(self, products, **kwargs):
        pass
