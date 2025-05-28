from products.Build.build_factory import BuildFactory
from products.CPU.cpu_factory import CPUFactory
from products.GPU.gpu_factory import GPUFactory
from products.Motherboard.motherboard_factory import MotherboardFactory
from products.RAM.ram_factory import RAMFactory
from products.Case.case_factory import CaseFactory
from products.PSU.psu_factory import PSUFactory

# Загрузка данных продуктов из JSON
CPU_json = CPUFactory.load_cpus_from_json('data/cards/cpus.json')
GPU_json = GPUFactory.load_gpus_from_json('data/cards/gpus.json')
Motherboard_json = MotherboardFactory.load_motherboards_from_json('data/cards/motherboards.json')
RAM_json = RAMFactory.load_rams_from_json('data/cards/rams.json')
Case_json = CaseFactory.load_cases_from_json('data/cards/cases.json')
PSU_json = PSUFactory.load_psus_from_json('data/cards/psus.json')
Builds_json = BuildFactory.load_builds_from_json('data/cards/builds.json')