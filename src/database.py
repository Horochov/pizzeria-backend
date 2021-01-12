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

    def connection_start(self):
        connection = psycopg2.connect(dbname="postgres",
                                      user=f"{self.user}",
                                      password=f"{self.password}")
        cursor = connection.cursor()
        return connection, cursor

    def connection_end(self, connection, cursor):
        if connection is not None:
            connection.commit()
        else:
            return

        if cursor is not None:
            cursor.close()
        else:
            return

        connection.close()

    def get_products(self):
        connection, cursor = self.connection_start()
        cursor.execute("""SELECT * FROM public.menu;""")
        products = cursor.fetchall()
        self.connection_end(connection, cursor)
        return products

    def add_orders(self, orders):
        [firstname, lastname] = orders['waiter'].split()
        client_name = orders['clientName']
        table_number = int(orders['table'])
        ordered_products = orders['order']

        connection, cursor = self.connection_start()

        # znalezienie id kelnera
        cursor.execute(f"""SELECT id FROM public.employees
        WHERE firstname='{firstname}' AND lastname='{lastname}';""")
        waiter_id = cursor.fetchone()[0]
        print(waiter_id)

        # obecna data i godzina
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(timestamp)

        # wstawienie nowego rachunku i otrzymanie jego id
        cursor.execute(f"""INSERT INTO public.bills
        (clientname, tablenr, waiterid)
        VALUES
        ('{client_name}', {table_number}, {waiter_id}) 
        RETURNING id;""")
        bill_id = cursor.fetchone()[0]
        print(bill_id)

        # wydobycie z bazy id wszystkich kucharzy
        #cursor.execute("SELECT id FROM public.employees WHERE jobtitle='Cook'")
        #cooks_id = []
        #for tuplee in cursor.fetchall():
            #cooks_id.append(tuplee[0])

        # dodanie zamówionych produktów do zamówień, i przypisanie losowego kucharza
        for product in ordered_products:
            if 'comment' in product.keys():
                comment = product['comment']
            else:
                comment = ""
            print(f"{product}: {comment}")
            cursor.execute(f"""INSERT INTO public.orders
            (status, comments, orderdate, billid, productid, cookid)
            VALUES
            (1, '{comment}', '{timestamp}', {bill_id}, {product['productId']}, null)""")

        # obliczenie ceny zamówienia i wpisanie jej do bazy
        #cursor.execute(f"CALL restaurant_schema.calculate_bill_value({bill_id});")
        self.connection_end(connection, cursor)

    def login(self, user, password):
        [firstname, lastname] = user.split()
        connection, cursor = self.connection_start()
        cursor.execute(f"""SELECT id FROM public.employees
        WHERE firstname='{firstname}' AND lastname='{lastname}' 
            AND password='{password}';""")
        user_got = cursor.fetchall()
        self.connection_end(connection, cursor)
        if user_got:
            return True
        else:
            return False
