import requests
from backend import *
from unittest.mock import MagicMock
import unittest

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
        self.assertEqual(testLogin("JS","admin12345"), True)

    def test_login_fake_user(self):
        self.assertEqual(testLogin("AB","admin12345"), False)
        
    def test_login_real_user_wrong_password(self):
        self.assertEqual(testLogin("JS","admin123456"), False)


if __name__ == '__main__':
    unittest.main()
