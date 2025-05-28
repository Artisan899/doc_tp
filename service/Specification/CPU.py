from service.BaseSpecification import BaseSpecification

class ManufacturerSpecification(BaseSpecification):
    def __init__(self, manufacturers=None):
        self.manufacturers = manufacturers or []

    def apply_filter(self, products, **kwargs):
        if not self.manufacturers:
            return products
        return [p for p in products if any(m.lower() in p.name.lower() for m in self.manufacturers)]

class FrequencySpecification(BaseSpecification):
    def __init__(self, frequencies=None):
        self.frequencies = frequencies or []

    def apply_filter(self, products, **kwargs):
        if not self.frequencies:
            return products

        def matches_freq(p):
            for f in self.frequencies:
                if p.frequency.startswith(f):
                    return True
            return False
        return [p for p in products if matches_freq(p)]

class SocketSpecification(BaseSpecification):
    def __init__(self, sockets=None):
        self.sockets = sockets or []

    def apply_filter(self, products, **kwargs):
        if not self.sockets:
            return products
        return [p for p in products if p.socket in self.sockets]


class CoreCountSpecification(BaseSpecification):
    def __init__(self, cores=None):
        self.cores = cores if cores else []

    def apply_filter(self, products, **kwargs):
        if not self.cores:
            return products
        return [p for p in products if hasattr(p, 'cores') and p.cores in self.cores]
