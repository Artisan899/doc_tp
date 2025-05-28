import json
from datetime import datetime
import uuid

class Order:
    def __init__(
        self, user_email, full_name, phone, address,
        total_amount, bonus_earned, bonus_spent,
        delivery_date, items,
        order_date=None, order_id=None
    ):
        self.id = order_id if order_id else str(uuid.uuid4())
        self.user_email = user_email
        self.full_name = full_name
        self.phone = phone
        self.address = address
        self.total_amount = total_amount
        self.bonus_earned = bonus_earned
        self.bonus_spent = bonus_spent
        self.delivery_date = delivery_date
        self.items = items  # список словарей с id, name, quantity
        self.order_date = order_date if order_date else datetime.now().strftime("%d-%m-%Y %H:%M:%S")


    def to_dict(self):
        return {
            "id": self.id,
            "user_email": self.user_email,
            "full_name": self.full_name,
            "phone": self.phone,
            "address": self.address,
            "total_amount": self.total_amount,
            "bonus_earned": self.bonus_earned,
            "bonus_spent": self.bonus_spent,
            "delivery_date": self.delivery_date,
            "items": self.items,
            "order_date": self.order_date,

        }

    @staticmethod
    def save_to_json(orders, filename="data/orders.json"):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([order.to_dict() for order in orders], f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_from_json(filename="data/orders.json"):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [
                    Order(
                        user_email=order['user_email'],
                        full_name=order['full_name'],
                        phone=order['phone'],
                        address=order['address'],
                        total_amount=order['total_amount'],
                        bonus_earned=order['bonus_earned'],
                        bonus_spent=order['bonus_spent'],
                        delivery_date=order['delivery_date'],
                        items=order.get('items', []),
                        order_date=order.get('order_date'),
                        order_id=order.get('id'),

                    ) for order in data
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
