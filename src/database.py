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
    def __init__(self, user, password, dbname = "postgres", schema_name = "public"):
        self.user = user
        self.password = password
        self.dbname = dbname
        self.schema_name = schema_name

    def connection_start(self):
        connection = psycopg2.connect(dbname=f"{self.dbname}",
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
        cursor.execute(f"""SELECT * FROM {self.schema_name}.menu;""")
        products = cursor.fetchall()
        self.connection_end(connection, cursor)
        return products

    def add_orders(self, orders):
        user = orders['waiter']
        password = orders['waiterPassword']
        client_name = orders['clientName']
        table_number = int(orders['table'])
        ordered_products = orders['order']
        
        #pobierz ID kelnera (i sprawdź uprawnienia)
        waiter_id = self.login(user, password)
        if not waiter_id:
            print(f"Failed to authenticate {user}!")
            return False
        
        connection, cursor = self.connection_start()

        # obecna data i godzina
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(timestamp)

        #sprawdź czy rachunek dla stolika i imienia jest otwarty
        cursor.execute(f"""SELECT id FROM {self.schema_name}.bills
        WHERE clientname='{client_name}' AND tablenr={table_number} AND billvalue>0""")
        bill_id = cursor.fetchone()
        if(bill_id != None):
            bill_id=bill_id[0]
        else:
            # wstawienie nowego rachunku i otrzymanie jego id
            cursor.execute(f"""INSERT INTO {self.schema_name}.bills
            (clientname, tablenr, waiterid)
            VALUES
            ('{client_name}', {table_number}, {waiter_id}) 
            RETURNING id;""")
            bill_id = cursor.fetchone()[0]
        print(bill_id)
        
        # dodanie zamówionych produktów do zamówień
        for product in ordered_products:
            if 'comment' in product.keys():
                comment = product['comment']
            else:
                comment = ""
            print(f"{product}: {comment}")
            cursor.execute(f"""INSERT INTO {self.schema_name}.orders
            (status, comments, orderdate, billid, productid, cookid)
            VALUES
            (1, '{comment}', '{timestamp}', {bill_id}, {product['productId']}, null)""")

        self.connection_end(connection, cursor)
        return True

    #jeżeli podano prawidłowe dane zwraca ID pracownika
    #w przeciwnym razie zwraca None
    def login(self, user, password):
        [firstname, lastname] = user.split()
        connection, cursor = self.connection_start()
        cursor.execute(f"""SELECT id FROM {self.schema_name}.employees
        WHERE firstname='{firstname}' AND lastname='{lastname}' 
            AND password='{password}';""")
        user_got = cursor.fetchone()
        self.connection_end(connection, cursor)
        if user_got:
            return user_got[0]
        else:
            return None
