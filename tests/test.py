import unittest
from user.models import User
from products.CPU.cpu_factory import CPUFactory
import os


class TestShop(unittest.TestCase):

    def test_user_add_to_cart(self):
        user = User('testuser', 'test@example.com', 'pass123')
        user.add_to_cart('cpu', 'cpu001', 3)

        print("\n[TEST] Корзина пользователя:", user.cart)

        self.assertIn('cpu_cpu001', user.cart)
        self.assertEqual(user.cart['cpu_cpu001'], 3)

    def test_load_cpus_from_json(self):
        base_dir = os.path.dirname(__file__)
        json_path = os.path.join(base_dir, '..', 'data', 'cards', 'cpus.json')
        cpus = CPUFactory.load_cpus_from_json(os.path.abspath(json_path))

        print(f"\n[TEST] Загружено процессоров: {len(cpus)}")
        print(f"[TEST] Первый процессор: {cpus[0].name}")

        self.assertIsInstance(cpus, list)
        self.assertGreater(len(cpus), 0)
        self.assertTrue(hasattr(cpus[0], 'name'))

    def test_clear_cart(self):
        user = User('testuser', 'test@example.com', 'pass123')
        user.add_to_cart('gpu', 'gpu001', 1)
        user.add_to_cart('cpu', 'cpu002', 2)

        print("\n[TEST] Корзина до очистки (товар и количество:", user.cart)
        user.clear_cart()
        print("[TEST] Корзина после очистки:", user.cart)

        self.assertEqual(user.cart, {})


if __name__ == '__main__':
    unittest.main()
