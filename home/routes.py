from flask import Blueprint, render_template, session
import json
from user.routes import UserService
from service.product_data import Builds_json, GPU_json, CPU_json, Motherboard_json, RAM_json, Case_json, PSU_json

home_bp = Blueprint('home', __name__, url_prefix='')

# Инициализируем UserService (путь к файлу с пользователями можно вынести в config)
user_service = UserService("data/users.json")

@home_bp.route('/home')
def home():
    try:
        # Загружаем хиты продаж
        with open('data/hit_products.json', 'r') as f:
            hit_list = json.load(f)['hit_products']

        # Получаем корзину и статус аутентификации
        cart = {}
        is_authenticated = False

        if 'username' in session:
            user = user_service.get_user(session['username'])
            cart = user.cart
            is_authenticated = True

        hit_products = []
        for item in hit_list:
            product = None
            product_type = None

            if item['type'] == 'PC':
                product = next((b for b in Builds_json if b.id == item['id']), None)
                product_type = 'build'
            elif item['type'] == 'GPU':
                product = next((g for g in GPU_json if g.id == item['id']), None)
                product_type = 'gpu'
            elif item['type'] == 'CPU':
                product = next((c for c in CPU_json if c.id == item['id']), None)
                product_type = 'cpu'
            elif item['type'] == 'Motherboard':
                product = next((m for m in Motherboard_json if m.id == item['id']), None)
                product_type = 'motherboard'
            elif item['type'] == 'RAM':
                product = next((r for r in RAM_json if r.id == item['id']), None)
                product_type = 'ram'
            elif item['type'] == 'Case':
                product = next((cs for cs in Case_json if cs.id == item['id']), None)
                product_type = 'case'
            elif item['type'] == 'PSU':
                product = next((p for p in PSU_json if p.id == item['id']), None)
                product_type = 'psu'

            if product:
                hit_products.append({
                    'product': product,
                    'type': product_type
                })

        return render_template('home.html',
                               hit_products=hit_products,
                               cart=cart,
                               is_authenticated=is_authenticated)

    except Exception as e:
        print(f"Error loading hit products: {str(e)}")
        return render_template('home.html',
                               hit_products=[],
                               cart={},
                               is_authenticated=False)
