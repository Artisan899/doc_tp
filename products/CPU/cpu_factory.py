import json
from products.CPU.cpu import CPU

class CPUFactory:
    @staticmethod
    def load_cpus_from_json(path):
        cpus = []
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            images = item.get('images') or [item.get('image')]
            cpu = CPU(
                id=item['id'],
                name=item['name'],
                price=item['price'],
                category=item.get('category', 'cpu'),
                frequency=item['frequency'],
                socket=item['socket'],
                cores=item['cores'],
                cpu_type=item.get('type', ''),
                images=images
            )
            cpus.append(cpu)
        return cpus
