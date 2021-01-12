from flask import Flask, request, jsonify
import simplejson
import hashlib
from database import PizzeriaRepository


def main():

    app = Flask(__name__)

    repo = PizzeriaRepository("restaurant", "123456")

    @app.route('/menu', methods=['GET'])
    def select_menu():
        products = repo.get_products()
        json_products = simplejson.dumps(products)
        return json_products

    @app.route('/addorder', methods=['POST'])
    def add_order():
        orders = request.json
        added = repo.add_orders(orders) 
        return jsonify(added)

    @app.route('/user', methods=['POST'])
    def login():
        user = request.json
        nickname = user['nickname']
        password = user["password"]
        logged_in = bool(repo.login(nickname, password))
        return jsonify(logged_in)

    app.run()

if __name__ == '__main__':
    main()
