import psycopg2
import random
import datetime
from abc import ABC, abstractmethod


class AbstractPizzeriaRepository(ABC):
    @abstractmethod
    def get_products(self):
        pass

    @abstractmethod
    def add_orders(self, order):
        pass

    @abstractmethod
    def login(self, user, password):
        pass


class PizzeriaRepository(AbstractPizzeriaRepository):
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connection_start(self):
        self.connection = psycopg2.connect(dbname="restaurant",
                                           user=f"{self.user}",
                                           password=f"{self.password}")  # todo dbname=postgres u Radka
        self.cursor = self.connection.cursor()

    def connection_end(self):
        if self.connection is not None:
            self.connection.commit()
        else:
            return

        if self.cursor is not None:
            self.cursor.close()
        else:
            return

        self.connection.close()
        self.connection = None
        self.cursor = None

    def get_products(self):
        self.connection_start()
        self.cursor.execute("""SELECT * FROM restaurant_schema.products;""")
        products = self.cursor.fetchall()
        self.connection_end()
        return products

    def add_orders(self, orders):
        waiter_nickname = orders['waiter']
        client_name = orders['clientName']
        table_number = int(orders['table'])
        ordered_products = orders['order']

        self.connection_start()

        # znalezienie id kelnera
        self.cursor.execute(f"""SELECT id FROM restaurant_schema.employees
        WHERE nickname='{waiter_nickname}';""")
        waiter_id = self.cursor.fetchone()[0]

        # obecna data i godzina
        self.cursor.execute("SELECT CURRENT_TIMESTAMP;")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # wstawienie nowego rachunku i otrzymanie jego id
        self.cursor.execute(f"""INSERT INTO restaurant_schema.bills
        (client_name, table_number, bill_date, waiter_id)
        VALUES
        ('{client_name}', {table_number}, '{timestamp}', {waiter_id}) 
        RETURNING id;""")
        bill_id = self.cursor.fetchone()[0]

        # wydobycie z bazy id wszystkich kucharzy
        self.cursor.execute("SELECT id FROM restaurant_schema.employees WHERE job='Cook'")
        cooks_id = []
        for tuplee in self.cursor.fetchall():
            cooks_id.append(tuplee[0])

        # dodanie zamówionych produktów do zamówień, i przypisanie losowego kucharza
        for product in ordered_products:
            if 'comment' in product.keys():
                comment = product['comment']
            else:
                comment = ""
            self.cursor.execute(f"""INSERT INTO restaurant_schema.orders
            (order_comment, order_date, bill_id, product_id, cook_id)
            VALUES
            ('{comment}', '{timestamp}', {bill_id}, {product['productId']}, {random.choice(cooks_id)})""")

        # obliczenie ceny zamówienia i wpisanie jej do bazy
        self.cursor.execute(f"CALL restaurant_schema.calculate_bill_value({bill_id});")

        self.connection.commit()
        self.connection_end()

    def login(self, user, password):
        self.connection_start()
        self.cursor.execute(f"""SELECT * FROM restaurant_schema.employees
        WHERE nickname='{user}' AND employee_password='{password}';""")
        user_got = self.cursor.fetchall()
        self.connection_end()
        if user_got:
            return True
        else:
            return False
