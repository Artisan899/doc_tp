from service.BaseSpecification import BaseSpecification

class CaseColorSpecification(BaseSpecification):
    def __init__(self, colors=None):
        self.colors = colors if colors else []

    def apply_filter(self, products, **kwargs):
        if not self.colors:
            return products
        return [p for p in products if hasattr(p, 'color') and p.color in self.colors]


class CaseFormFactorSpecification(BaseSpecification):
    def __init__(self, form_factors=None):
        self.form_factors = form_factors if form_factors else []

    def apply_filter(self, products, **kwargs):
        if not self.form_factors:
            return products
        return [p for p in products if hasattr(p, 'form_factor') and p.form_factor in self.form_factors]
