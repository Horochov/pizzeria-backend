import requests
from backend import *
from unittest.mock import MagicMock
import unittest
import hashlib
import database

repo = PizzeriaRepository("postgres", "postgres")

def testLogin(user, password):
    headers = {"Accept": "application/json",
              "Content-Type": "application/json"
              }
    
    address = 'http://127.0.0.1:5000/user'
    
    data = {
            'nickname': user,
            'password': password
            }
        
    r = requests.post(address, headers=headers, json=data)
    return r.json() == True

class TestStringMethods(unittest.TestCase):

    def test_login_real_user(self):
        user = "JS"
        password = "admin12345"
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.assertEqual(repo.login(user,password), True)
        
    def test_login_fake_user(self):
        user = "AB"
        password = "admin12345"
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.assertEqual(repo.login(user,password), False)
        
        
    def test_login_real_user_wrong_password(self):
        user = "AB"
        password = "admin123456"
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.assertEqual(repo.login(user,password), False)
        
    
    def test_login_server_real_user(self):
        self.assertEqual(testLogin("JS","admin12345"), True)

    def test_login_server_fake_user(self):
        self.assertEqual(testLogin("AB","admin12345"), False)
        
    def test_login_server_real_user_wrong_password(self):
        self.assertEqual(testLogin("JS","admin123456"), False)


if __name__ == '__main__':
    unittest.main()
