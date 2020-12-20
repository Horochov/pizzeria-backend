import flask
import psycopg2
import simplejson


def main():
    app = flask.Flask("")

    @app.route('/menu')
    def select():
        connection = psycopg2.connect(dbname="restaurant", user="postgres", password="postgres")
        cursor = connection.cursor()

        cursor.execute("""SELECT * FROM restaurant_schema.products""")
        products = cursor.fetchall()
        json_products = simplejson.dumps(products)

        connection.commit()
        cursor.close()
        connection.close()
        return json_products

    app.run()


if __name__ == '__main__':
    main()
