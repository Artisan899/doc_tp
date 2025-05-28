from abc import ABC, abstractmethod

class BaseProduct(ABC):
    def __init__(self, id, name, price, category):
        self.id = id
        self.name = name
        self.price = price
        self.category = category

    @abstractmethod
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category': self.category,
        }
