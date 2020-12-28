import psycopg2
from abc import ABC, abstractmethod


class AbstractPizzeriaRepository(ABC):
    @abstractmethod
    def get_products(self):
        pass


class PizzeriaRepository(AbstractPizzeriaRepository):
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connection_start(self):
        self.connection = psycopg2.connect(dbname="restaurant", user=f"{self.user}",
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
        self.cursor.execute("""SELECT * FROM restaurant_schema.products""")
        products = self.cursor.fetchall()
        self.connection_end()
        return products
