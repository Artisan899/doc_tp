from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from user.services import UserService

user_bp = Blueprint('user', __name__, url_prefix='/user', template_folder='../../templates/login_register')

user_service = UserService("data/users.json")

@user_bp.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Пароли не совпадают", 'danger')
            return redirect(url_for('user.register_page'))

        if user_service.is_email_taken(email):
            flash("Пользователь с таким email уже существует", 'danger')
            return redirect(url_for('user.register_page'))

        try:
            user_service.add_user(username, email, password)
            flash("Регистрация успешна! Вам начислено 1000 бонусных баллов.", 'success')
            return redirect(url_for('user.login'))
        except Exception as e:
            flash(f"Ошибка при регистрации: {str(e)}", 'danger')
            return redirect(url_for('user.register_page'))
    else:
        return render_template('login_register/register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = user_service.get_user(username)

        if not user:
            flash("Пользователь с таким именем не найден", 'danger')
        elif not user_service.check_password(user.password, password):
            flash("Неверный пароль", 'danger')
        else:
            session['username'] = user.username
            flash("Вход успешен!", 'success')
            return redirect(url_for('home.home'))

    return render_template('login_register/login.html')

@user_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash("Вы успешно вышли из системы", 'success')
    return redirect(url_for('home.home'))
