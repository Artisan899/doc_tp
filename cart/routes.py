from flask import Blueprint, session, flash, redirect, url_for, render_template, request, jsonify
from user.services import UserService

from service.product_data import GPU_json, Builds_json, CPU_json, Case_json, Motherboard_json, RAM_json, PSU_json

user_service = UserService("data/users.json")

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
def cart():
    if 'username' not in session:
        flash('Для просмотра корзины необходимо войти в систему', 'warning')
        return redirect(url_for('user.login'))

    user = user_service.get_user(session['username'])
    if not user:
        flash('Пользователь не найден', 'danger')
        return redirect(url_for('home'))

    cart_items = []
    for key, quantity in user.cart.items():
        product_type, product_id = key.split('_', 1)

        product = None
        images = []
        if product_type == 'gpu':
            product = next((g for g in GPU_json if g.id == product_id), None)
            images = product.images if product else []
        elif product_type == 'build':
            product = next((b for b in Builds_json if b.id == product_id), None)
            images = product.images if product else []
        elif product_type == 'cpu':
            product = next((c for c in CPU_json if c.id == product_id), None)
            images = product.images if product else []
        elif product_type == 'Motherboard':
            product = next((m for m in Motherboard_json if m.id == product_id), None)
            images = product.images if product else []
        elif product_type == 'ram':
            product = next((r for r in RAM_json if r.id == product_id), None)
            images = product.images if product else []
        elif product_type == 'case':
            product = next((cs for cs in Case_json if cs.id == product_id), None)
            images = product.images if product else []
        elif product_type == 'psu':
            product = next((p for p in PSU_json if p.id == product_id), None)
            images = product.images if product else []

        if product:
            cart_items.append({
                'product': product,
                'type': product_type,
                'quantity': quantity,
                'images': images,
                'cart_key': key
            })

    total = sum(item['product'].price * item['quantity'] for item in cart_items)

    return render_template('cart.html',
                           cart_items=cart_items,
                           total=total,
                           user=user,
                           is_authenticated=True)


@cart_bp.route('/clear_cart', methods=['POST'])
def clear_cart():
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    user = user_service.get_user(session['username'])
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404

    user.clear_cart()
    user_service.update_user(user)

    return jsonify({
        'success': True,
        'cart_count': 0,
        'message': 'Корзина очищена'
    })


@cart_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    try:
        product_id = request.form.get('product_id')
        product_type = request.form.get('product_type')

        if not product_id or not product_type:
            return jsonify({'success': False, 'error': 'Missing products data'}), 400

        user = user_service.get_user(session['username'])
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        user.add_to_cart(product_type, product_id)
        user_service.update_user(user)

        return jsonify({
            'success': True,
            'cart_count': user.get_cart_count()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@cart_bp.route('/update_cart', methods=['POST'])
def update_cart():
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    product_id = request.form.get('product_id')
    product_type = request.form.get('product_type')
    quantity = int(request.form.get('quantity', 1))

    user = user_service.get_user(session['username'])
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404

    user.update_cart_item(product_type, product_id, quantity)
    user_service.update_user(user)

    return jsonify({
        'success': True,
        'cart_count': user.get_cart_count()
    })


@cart_bp.route('/get_cart_count')
def get_cart_count():
    if 'username' not in session:
        return jsonify({'cart_count': 0})

    user = user_service.get_user(session['username'])
    if not user:
        return jsonify({'cart_count': 0})

    return jsonify({
        'cart_count': user.get_cart_count()
    })
