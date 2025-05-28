from service.BaseSpecification import BaseSpecification

class PSUCeritificateSpecification(BaseSpecification):
    def __init__(self, certificates=None):
        self.certificates = certificates if certificates else []

    def apply_filter(self, products, **kwargs):
        if not self.certificates:
            return products
        return [p for p in products if hasattr(p, 'certificate') and p.certificate in self.certificates]


class PSUPowerSpecification(BaseSpecification):
    def __init__(self, powers=None):
        self.powers = powers if powers else []

    def apply_filter(self, products, **kwargs):
        if not self.powers:
            return products
        return [p for p in products if hasattr(p, 'power') and str(p.power) in self.powers]


class PSUTypeSpecification(BaseSpecification):
    def __init__(self, types=None):
        self.types = types if types else []

    def apply_filter(self, products, **kwargs):
        if not self.types:
            return products
        return [p for p in products if hasattr(p, 'type') and p.type in self.types]
