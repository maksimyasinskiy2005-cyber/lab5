import os
import unittest
from app import app
from tinydb import TinyDB

class ProductsTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

        # Тимчасова БД для тестування
        self.test_db_path = 'data/test_products.json'
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        
        import products.routes
        products.routes.get_db = lambda: TinyDB(self.test_db_path)

    def tearDown(self):
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_create_and_read_product(self):
        """Тест додавання та перегляду товару"""
        response = self.client.post('/product/add', data={
            'name': 'Тестовий телефон',
            'content': 'Детальний опис тестового смартфона',
            'price': '19999.99',
            'category': 'electronics',
            'quantity': 5
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Тестовий телефон'.encode('utf-8'), response.data)

        # Перевірка детальної сторінки
        response_detail = self.client.get('/product/1')
        self.assertEqual(response_detail.status_code, 200)
        self.assertIn('Детальний опис тестового смартфона'.encode('utf-8'), response_detail.data)

    def test_update_product(self):
        """Тест редагування товару"""
        self.client.post('/product/add', data={
            'name': 'Стара назва',
            'content': 'Старий опис товару',
            'price': '100.00',
            'category': 'books',
            'quantity': 2
        })

        response = self.client.post('/product/1/edit', data={
            'name': 'Нова назва',
            'content': 'Оновлений опис товару',
            'price': '150.00',
            'category': 'books',
            'quantity': 10
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Нова назва'.encode('utf-8'), response.data)

    def test_delete_product(self):
        """Тест видалення товару"""
        self.client.post('/product/add', data={
            'name': 'Товар для видалення',
            'content': 'Короткий опис',
            'price': '50.00',
            'category': 'home',
            'quantity': 1
        })

        response = self.client.post('/product/1/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_not_found = self.client.get('/product/1')
        self.assertEqual(response_not_found.status_code, 404)

if __name__ == '__main__':
    unittest.main()
