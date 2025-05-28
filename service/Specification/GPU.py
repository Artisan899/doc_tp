from service.BaseSpecification import BaseSpecification

class MemorySpecification(BaseSpecification):
    def __init__(self, min_memory=None):
        self.min_memory = min_memory

    def apply_filter(self, items):
        if self.min_memory is None:
            return items
        return [i for i in items if i.memory >= self.min_memory]


class MemoryTypeSpecification(BaseSpecification):
    def __init__(self, memory_types=None):
        self.memory_types = memory_types or []

    def apply_filter(self, items):
        if not self.memory_types:
            return items
        return [i for i in items if i.memory_type in self.memory_types]


class ClockSpeedSpecification(BaseSpecification):
    def __init__(self, min_clock_speed=None):
        self.min_clock_speed = min_clock_speed

    def apply_filter(self, items):
        if self.min_clock_speed is None:
            return items
        return [i for i in items if i.clock_speed >= self.min_clock_speed]