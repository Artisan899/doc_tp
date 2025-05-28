# user/services.py
import json
import bcrypt
from typing import Optional, Dict
from user.models import User


class UserService:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = f.read().strip()
                if not data:
                    with open(self.filepath, 'w', encoding='utf-8') as f:
                        json.dump([], f, ensure_ascii=False)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False)

    def _load_users(self) -> list[dict]:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_users(self, users: list[dict]):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

    def add_user(self, username: str, email: str, password: str):
        users = self._load_users()
        if any(user['email'] == email for user in users):
            raise ValueError("Пользователь с таким email уже существует.")

        new_user = User(username, email, password)
        users.append(new_user.to_dict())
        self._save_users(users)

    def get_user(self, username_or_email: str) -> Optional[User]:
        users = self._load_users()
        for user_data in users:
            if user_data['username'] == username_or_email or user_data['email'] == username_or_email:
                return User.from_dict(user_data)
        return None

    def update_user(self, user: User):
        users = self._load_users()
        updated_users = []
        found = False

        for user_data in users:
            if user_data['username'] == user.username:
                updated_users.append(user.to_dict())
                found = True
            else:
                updated_users.append(user_data)

        if not found:
            updated_users.append(user.to_dict())

        self._save_users(updated_users)

    def check_password(self, stored_password: str, provided_password: str) -> bool:
        try:
            return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))
        except Exception as e:
            print(f"Error checking password: {e}")
            return False

    def is_email_taken(self, email: str) -> bool:
        users = self._load_users()
        return any(user['email'] == email for user in users)

    def add_bonus_points(self, username: str, points: int):
        """Добавляет бонусные баллы пользователю"""
        user = self.get_user(username)
        if user:
            user.bonus_card['points'] += points
            self.update_user(user)
            return True
        return False

    def minus_bonus_points(self, username: str, points: int):
        user = self.get_user(username)
        if user:
            user.bonus_card['points'] -= points
            self.update_user(user)
            return True
        return False
