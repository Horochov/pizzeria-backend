from flask import Flask, request, jsonify
import simplejson
import hashlib
from database import PizzeriaRepository

class Backend:
    app = Flask(__name__)
    repo = PizzeriaRepository("postgres", "postgres")
    
    def main(self,port=5000):
        @self.app.route('/menu', methods=['GET'])
        def select_menu():
            products = self.repo.get_products()
            json_products = simplejson.dumps(products)
            print(json_products)
            return json_products

        @self.app.route('/addorder', methods=['POST'])
        def add_order():
            orders = request.json
            self.repo.add_orders(orders)
            return jsonify(True)

        @self.app.route('/user', methods=['POST'])
        def login():
            user = request.json
            nickname = user['nickname']
            password = hashlib.sha256(user["password"].encode('utf-8')).hexdigest()
            logged_in = self.repo.login(nickname, password)
            return jsonify(logged_in)

        self.app.run(port=port)

if __name__ == '__main__':
    Backend().main()
