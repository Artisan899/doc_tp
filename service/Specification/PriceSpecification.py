from service.BaseSpecification import BaseSpecification

class PriceSpecification(BaseSpecification):
    def __init__(self, min_price=None, max_price=None):
        self.min_price = min_price
        self.max_price = max_price

    def apply_filter(self, products, **kwargs):
        filtered = []
        for p in products:
            if self.min_price is not None and p.price < self.min_price:
                continue
            if self.max_price is not None and p.price > self.max_price:
                continue
            filtered.append(p)
        return filtered
