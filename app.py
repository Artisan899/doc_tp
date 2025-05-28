from flask import Flask, redirect, url_for

# Роуты
from user.routes import UserService
from user.routes import user_bp
from products.routes import products_bp
from cart.routes import cart_bp
from order.routes import order_bp
from home.routes import home_bp

app = Flask(__name__)

app.secret_key = 'your_secret_key'

#Загрузка пользователей
user_service = UserService("data/users.json")

@app.route('/')
def index():
    return redirect(url_for('home.home'))

#Регистрация_Вход
app.register_blueprint(user_bp)

#Домашняя страница
app.register_blueprint(home_bp)

#Разделы/Категории
app.register_blueprint(products_bp)

#Корзина
app.register_blueprint(cart_bp)

#Оформление заказа
app.register_blueprint(order_bp)


if __name__ == '__main__':
    app.run(debug=True, port=8080)