from flask import Blueprint, render_template, session, request
from user.services import UserService
from service.product_data import *

from service.Specification.PriceSpecification import PriceSpecification
from service.Specification.RAM import RamTypeSpecification, RamSpeedSpecification
from service.Specification.Motherboard import MotherboardSocketSpecification, MotherboardMemorySupportSpecification
from service.Specification.CASE import CaseColorSpecification, CaseFormFactorSpecification
from service.Specification.PSU import PSUTypeSpecification, PSUPowerSpecification, PSUCeritificateSpecification
from service.Specification.CPU import ManufacturerSpecification, FrequencySpecification, SocketSpecification, CoreCountSpecification
from service.Specification.GPU import MemorySpecification, MemoryTypeSpecification, ClockSpeedSpecification

user_service = UserService("data/users.json")

products_bp = Blueprint('products', __name__, url_prefix='', template_folder='../templates/products')



@products_bp.route('/builds')
def builds():
    builds = BuildFactory.load_builds_from_json('data/cards/builds.json')

    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)

    specs = []
    if min_price is not None or max_price is not None:
        specs.append(PriceSpecification(min_price, max_price))

    filtered_builds = builds
    for spec in specs:
        filtered_builds = spec.apply_filter(filtered_builds)

    cart, auth = get_cart_and_auth()

    return render_template('products/builds.html', builds=filtered_builds, cart=cart, is_authenticated=auth)


@products_bp.route('/gpus')
def gpus():
    gpus = GPUFactory.load_gpus_from_json('data/cards/gpus.json')

    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    min_memory = request.args.get('min_memory', type=int)
    memory_types = request.args.getlist('memory_type')
    min_clock_speed = request.args.get('min_clock_speed', type=int)

    specs = []

    if min_price is not None or max_price is not None:
        specs.append(PriceSpecification(min_price, max_price))
    if min_memory is not None:
        specs.append(MemorySpecification(min_memory))
    if memory_types:
        specs.append(MemoryTypeSpecification(memory_types))
    if min_clock_speed is not None:
        specs.append(ClockSpeedSpecification(min_clock_speed))

    filtered_gpus = gpus
    for spec in specs:
        filtered_gpus = spec.apply_filter(filtered_gpus)

    cart, auth = get_cart_and_auth()

    return render_template('products/gpus.html', gpus=filtered_gpus, cart=cart, is_authenticated=auth)

@products_bp.route('/cpus')
def cpus():
    cpus = CPUFactory.load_cpus_from_json('data/cards/cpus.json')

    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    manufacturers = request.args.getlist('manufacturer')
    frequencies = request.args.getlist('frequency')
    sockets = request.args.getlist('socket')
    cores = request.args.getlist('cores', type=int)  # список выбранных ядер, преобразуем в int

    specs = []
    if min_price is not None or max_price is not None:
        specs.append(PriceSpecification(min_price, max_price))
    if manufacturers:
        specs.append(ManufacturerSpecification(manufacturers))
    if frequencies:
        specs.append(FrequencySpecification(frequencies))
    if sockets:
        specs.append(SocketSpecification(sockets))
    if cores:
        specs.append(CoreCountSpecification(cores))

    filtered_cpus = cpus
    for spec in specs:
        filtered_cpus = spec.apply_filter(filtered_cpus)

    cart, auth = get_cart_and_auth()
    return render_template('products/cpus.html', cpus=filtered_cpus, cart=cart, product_type='cpu', is_authenticated=auth)


@products_bp.route('/motherboards')
def motherboards():
    motherboards = MotherboardFactory.load_motherboards_from_json('data/cards/motherboards.json')

    # Получаем параметры фильтра
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sockets = request.args.getlist('socket')
    memory_support = request.args.getlist('memory_support')

    # Формируем спецификации
    specs = []
    if min_price is not None or max_price is not None:
        specs.append(PriceSpecification(min_price, max_price))
    if sockets:
        specs.append(MotherboardSocketSpecification(sockets))
    if memory_support:
        specs.append(MotherboardMemorySupportSpecification(memory_support))

    # Применяем фильтры
    filtered_motherboards = motherboards
    for spec in specs:
        filtered_motherboards = spec.apply_filter(filtered_motherboards)

    # Получаем корзину и авторизацию
    cart, auth = get_cart_and_auth()

    return render_template(
        'products/motherboards.html',
        motherboards=filtered_motherboards,
        cart=cart,
        product_type='motherboard',
        is_authenticated=auth,
        selected_sockets=sockets,
        selected_memory_support=memory_support,
        request=request
    )


@products_bp.route('/rams')
def rams():
    rams = RAMFactory.load_rams_from_json('data/cards/rams.json')

    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    types = request.args.getlist('type')
    min_speed = request.args.get('min_speed', type=int)

    specs = []
    if min_price is not None or max_price is not None:
        specs.append(PriceSpecification(min_price, max_price))
    if types:
        specs.append(RamTypeSpecification(types))
    if min_speed is not None:
        specs.append(RamSpeedSpecification(min_speed))

    filtered_rams = rams
    for spec in specs:
        filtered_rams = spec.apply_filter(filtered_rams)

    cart, auth = get_cart_and_auth()
    return render_template('products/rams.html', rams=filtered_rams, cart=cart, product_type='ram', is_authenticated=auth)


@products_bp.route('/cases')
def cases():
    cases = CaseFactory.load_cases_from_json('data/cards/cases.json')

    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    colors = request.args.getlist('color')
    form_factors = request.args.getlist('form_factor')

    specs = []
    if min_price is not None or max_price is not None:
        specs.append(PriceSpecification(min_price, max_price))
    if colors:
        specs.append(CaseColorSpecification(colors))
    if form_factors:
        specs.append(CaseFormFactorSpecification(form_factors))

    filtered_cases = cases
    for spec in specs:
        filtered_cases = spec.apply_filter(filtered_cases)

    cart, auth = get_cart_and_auth()
    return render_template('products/cases.html', cases=filtered_cases, cart=cart, product_type='case', is_authenticated=auth)


@products_bp.route('/psus')
def psus():
    psus = PSUFactory.load_psus_from_json('data/cards/psus.json')

    # Получаем параметры из формы
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    selected_certs = request.args.getlist('certificate')
    selected_powers = request.args.getlist('power')
    selected_types = request.args.getlist('type')

    # Фильтрация
    specs = []
    if min_price is not None or max_price is not None:
        specs.append(PriceSpecification(min_price, max_price))
    if selected_certs:
        specs.append(PSUCeritificateSpecification(selected_certs))
    if selected_powers:
        specs.append(PSUPowerSpecification(selected_powers))
    if selected_types:
        specs.append(PSUTypeSpecification(selected_types))

    filtered_psus = psus
    for spec in specs:
        filtered_psus = spec.apply_filter(filtered_psus)

    cart, auth = get_cart_and_auth()

    # Для фильтрации на форме нужно собрать все возможные значения из исходного списка
    all_certificates = sorted(set(p.certificate for p in psus))
    all_powers = sorted(set(p.power for p in psus))
    all_types = sorted(set(p.type for p in psus))

    return render_template(
        'products/psus.html',
        psus=filtered_psus,
        cart=cart,
        product_type='psu',
        is_authenticated=auth,
        all_certificates=all_certificates,
        all_powers=all_powers,
        all_types=all_types,
    )


# Вспомогательная функция
def get_cart_and_auth():
    if 'username' not in session:
        return {}, False
    user = user_service.get_user(session['username'])
    return user.cart, True
