import requests
import flask
import psycopg2
import simplejson


def connection_start():
    connection = psycopg2.connect(dbname="restaurant", user="postgres", password="postgres")
    cursor = connection.cursor()
    return connection, cursor


def connection_end(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()


def database_get_products():
    connection, cursor = connection_start()

    cursor.execute("""SELECT * FROM restaurant_schema.products""")
    products = cursor.fetchall()

    connection_end(connection, cursor)

    return products


def main():
    app = flask.Flask("")

    @app.route('/menu')
    def select_menu():
        products = database_get_products()
        json_products = simplejson.dumps(products)
        return json_products

    # todo
    @app.route('/addorder', methods=['GET', 'POST'])
    def add_order():
        content = flask.request.json
        print(content)
        return content

    app.run()


if __name__ == '__main__':
    main()
