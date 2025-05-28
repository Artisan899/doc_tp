from service.BaseSpecification import BaseSpecification


class RamSpeedSpecification(BaseSpecification):
    def __init__(self, min_speed=None):
        self.min_speed = min_speed

    def apply_filter(self, products, **kwargs):
        filtered = []
        for p in products:
            if hasattr(p, 'speed'):
                if self.min_speed is not None and p.speed < self.min_speed:
                    continue
                filtered.append(p)
        return filtered


class RamTypeSpecification(BaseSpecification):
    def __init__(self, types=None):
        self.types = types if types else []

    def apply_filter(self, products, **kwargs):
        if not self.types:
            return products

        filtered = []
        for p in products:
            if hasattr(p, 'type'):
                if p.type in self.types:
                    filtered.append(p)
        return filtered