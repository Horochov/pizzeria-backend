from flask import Flask, request, jsonify
import simplejson
from src.database import PizzeriaRepository


def main():
    app = Flask(__name__)

    repo = PizzeriaRepository("postgres", "postgres")  # todo lepsze zabezpieczenia potem XD

    @app.route('/menu', methods=['GET'])
    def select_menu():
        products = repo.get_products()
        json_products = simplejson.dumps(products)
        print(json_products)
        return json_products

    # todo https://stackoverflow.com/questions/22947905/flask-example-with-post
    # todo https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application
    # todo https://blog.miguelgrinberg.com/post/restful-authentication-with-flask
    @app.route('/addorder', methods=['GET', 'POST'])
    def add_order():
        content = request.json
        print(content)
        return jsonify(content)

    app.run()


if __name__ == '__main__':
    main()
