import sqlite3
import hashlib

class Database:
    def __init__(self, db_name="company.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Создаем таблицы в базе данных"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Таблица цехов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS workshops (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
        ''')

        # Таблица продукции
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL,
                workshop_id INTEGER
            )
        ''')

        self.conn.commit()
        self.add_examples()

    def add_examples(self):
        """Добавляем примеры данных"""
        # Проверяем, есть ли цеха
        self.cursor.execute("SELECT COUNT(*) FROM workshops")
        if self.cursor.fetchone()[0] == 0:
            workshops = [
                ('Цех №1', 'Основной производственный цех'),
                ('Цех №2', 'Сборочный цех'),
                ('Цех №3', 'Упаковочный цех')
            ]
            self.cursor.executemany("INSERT INTO workshops (name, description) VALUES (?, ?)", workshops)

        self.cursor.execute("SELECT COUNT(*) FROM products")
        if self.cursor.fetchone()[0] == 0:
            products = [
                ('Телефон', 15000, 1),
                ('Наушники', 3000, 2),
                ('Чехол', 500, 3)
            ]
            self.cursor.executemany("INSERT INTO products (name, price, workshop_id) VALUES (?, ?, ?)", products)

        self.conn.commit()

    # Методы для пользователей
    def add_user(self, username, password):
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            self.conn.commit()
            return True
        except:
            return False

    def check_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, hashed_password)
        )
        return self.cursor.fetchone()

    # Методы для продукции
    def get_all_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def get_products_with_workshops(self):
        self.cursor.execute('''
            SELECT products.id, products.name, products.price, workshops.name as workshop_name 
            FROM products 
            LEFT JOIN workshops ON products.workshop_id = workshops.id
        ''')
        return self.cursor.fetchall()

    def add_product(self, name, price, workshop_id):
        try:
            self.cursor.execute(
                "INSERT INTO products (name, price, workshop_id) VALUES (?, ?, ?)",
                (name, price, workshop_id)
            )
            self.conn.commit()
            return True
        except:
            return False

    def get_all_workshops(self):
        self.cursor.execute("SELECT * FROM workshops")
        return self.cursor.fetchall()

    def add_workshop(self, name, description):
        try:
            self.cursor.execute(
                "INSERT INTO workshops (name, description) VALUES (?, ?)",
                (name, description)
            )
            self.conn.commit()
            return True
        except:
            return False
