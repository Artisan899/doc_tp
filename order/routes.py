from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from datetime import datetime, timedelta

# Импортируйте необходимые сервисы и данные
from user.services import UserService
from service.product_data import GPU_json, Builds_json, CPU_json, Motherboard_json, RAM_json, Case_json, PSU_json
from order.order import Order

user_service = UserService("data/users.json")

order_bp = Blueprint('order', __name__, url_prefix='/order', template_folder='../templates/order')


@order_bp.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'username' not in session:
        flash('Для оформления заказа необходимо войти в систему', 'warning')
        return redirect(url_for('login'))

    user = user_service.get_user(session['username'])
    if not user:
        flash('Пользователь не найден', 'danger')
        return redirect(url_for('home.home'))

    total = 0
    for key, quantity in user.cart.items():
        product_type, product_id = key.split('_', 1)
        product = None

        if product_type == 'gpu':
            product = next((g for g in GPU_json if g.id == product_id), None)
        elif product_type == 'build':
            product = next((b for b in Builds_json if b.id == product_id), None)
        elif product_type == 'cpu':
            product = next((c for c in CPU_json if c.id == product_id), None)
        elif product_type == 'Motherboard':
            product = next((m for m in Motherboard_json if m.id == product_id), None)
        elif product_type == 'ram':
            product = next((r for r in RAM_json if r.id == product_id), None)
        elif product_type == 'case':
            product = next((cs for cs in Case_json if cs.id == product_id), None)
        elif product_type == 'psu':
            product = next((p for p in PSU_json if p.id == product_id), None)

        if product:
            total += product.price * quantity

    bonus_earned = int(total * 0.15)

    if request.method == 'POST':
        use_bonus = 'use_bonus' in request.form

        if 'confirm_order' in request.form:
            if use_bonus:
                bonus_to_use = min(user.bonus_card['points'], max(total - 1, 0))
            else:
                bonus_to_use = 0

            final_amount = max(1, total - bonus_to_use)
            delivery_date = (datetime.now() + timedelta(days=14)).strftime("%d-%m-%Y") + " с 12:00 до 20:00"

            full_name = request.form.get('full_name')
            phone = request.form.get('phone')
            email = request.form.get('email')
            address = request.form.get('address')

            items = []
            for key, quantity in user.cart.items():
                product_type, product_id = key.split('_', 1)
                product = None

                if product_type == 'gpu':
                    product = next((g for g in GPU_json if g.id == product_id), None)
                elif product_type == 'build':
                    product = next((b for b in Builds_json if b.id == product_id), None)
                elif product_type == 'cpu':
                    product = next((c for c in CPU_json if c.id == product_id), None)
                elif product_type == 'Motherboard':
                    product = next((m for m in Motherboard_json if m.id == product_id), None)
                elif product_type == 'ram':
                    product = next((r for r in RAM_json if r.id == product_id), None)
                elif product_type == 'case':
                    product = next((cs for cs in Case_json if cs.id == product_id), None)
                elif product_type == 'psu':
                    product = next((p for p in PSU_json if p.id == product_id), None)

                if product:
                    items.append({
                        'type': product_type,
                        'id': product.id,
                        'name': getattr(product, 'name', 'Товар'),
                        'price': product.price,
                        'quantity': quantity
                    })

            order = Order(
                user_email=email,
                full_name=full_name,
                phone=phone,
                address=address,
                total_amount=final_amount,
                bonus_earned=bonus_earned,
                bonus_spent=bonus_to_use,
                delivery_date=delivery_date,
                items=items
            )

            orders = Order.load_from_json()
            orders.append(order)
            Order.save_to_json(orders)

            if use_bonus:
                user.bonus_card['points'] -= bonus_to_use
            user.bonus_card['points'] += bonus_earned

            user.clear_cart()
            user_service.update_user(user)

            flash(f'Заказ успешно оформлен! Вам начислено {bonus_earned} бонусных баллов', 'success')
            return redirect(url_for('home.home'))

        else:
            if use_bonus:
                bonus_to_use = min(user.bonus_card['points'], max(total - 1, 0))
            else:
                bonus_to_use = 0

    else:
        use_bonus = False
        bonus_to_use = 0

    delivery_date = (datetime.now() + timedelta(days=14)).strftime("%d-%m-%Y") + " с 12:00 до 20:00"
    max_bonus_to_use = min(user.bonus_card['points'], max(total - 1, 0))

    return render_template('payment.html',
                           user=user,
                           total=total,
                           bonus_to_use=bonus_to_use,
                           bonus_earned=bonus_earned,
                           bonus_spent=bonus_to_use,
                           delivery_date=delivery_date,
                           is_authenticated=True,
                           use_bonus=use_bonus,
                           max_bonus_to_use=max_bonus_to_use)
