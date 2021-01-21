import requests
from backend import *
from unittest.mock import MagicMock
import unittest
import hashlib
import database

# used in unit tests
repo = PizzeriaRepository("postgres", "postgres")

# check login method from PizzeriaRepository
def testLogin(user, password, rep = repo):
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return rep.login(user,password)

# check backend server login handling
# send and expect JSON data like frontend would
def testServerLogin(user, password):
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
    
    ##
    ## UNIT TESTS
    ##
    def test_login_real_user(self):
        self.assertEqual(testLogin("JS","admin12345"), True)
        
    def test_login_fake_user(self):
        self.assertEqual(testLogin("AB","admin12345"), False)
        
        
    def test_login_real_user_wrong_password(self):
        self.assertEqual(testLogin("JS","admin123456"), False)
        
    def test_login_mocked(self):
        repo2 = PizzeriaRepository("postgres", "postgres")
        repo2.login = MagicMock(return_value=True)
        self.assertEqual(testLogin("A","B", rep = repo2), True)

    ##
    ## ACCEPTANCE TESTS
    ##
    def test_login_server_real_user(self):
        self.assertEqual(testServerLogin("JS","admin12345"), True)

    def test_login_server_fake_user(self):
        self.assertEqual(testServerLogin("AB","admin12345"), False)
        
    def test_login_server_real_user_wrong_password(self):
        self.assertEqual(testServerLogin("JS","admin123456"), False)


if __name__ == '__main__':
    unittest.main()
