from service.BaseSpecification import BaseSpecification

class MotherboardSocketSpecification(BaseSpecification):
    def __init__(self, sockets=None):
        self.sockets = sockets if sockets else []

    def apply_filter(self, products, **kwargs):
        if not self.sockets:
            return products

        filtered = []
        for p in products:
            if hasattr(p, 'socket') and p.socket in self.sockets:
                filtered.append(p)
        return filtered

class MotherboardMemorySupportSpecification(BaseSpecification):
    def __init__(self, memory_support_list=None):
        self.memory_support_list = memory_support_list if memory_support_list else []

    def apply_filter(self, products, **kwargs):
        if not self.memory_support_list:
            return products

        filtered = []
        for p in products:
            if hasattr(p, 'memory_support') and p.memory_support in self.memory_support_list:
                filtered.append(p)
        return filtered
