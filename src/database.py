import flask
import psycopg2
import simplejson


def connection_start():
    connection = psycopg2.connect(dbname="postgres", user="postgres", password="postgres")
    cursor = connection.cursor()
    return connection, cursor


def connection_end(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()


def main():
    app = flask.Flask("")

    @app.route('/menu')
    def select_menu():
        connection, cursor = connection_start()

        cursor.execute("""SELECT * FROM restaurant_schema.products""")
        products = cursor.fetchall()
        json_products = simplejson.dumps(products)

        connection_end(connection, cursor)

        return json_products

    app.run()


if __name__ == '__main__':
    main()
