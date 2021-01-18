import requests

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

def tests():
    assert testLogin("JS","admin12345"), "Failed to log in to existing account"
    assert testLogin("BS","admin12345"), "Logged in to production (non-mock) account"
    assert testLogin("JSS","admin12345"), "Logged in to non-existing account (bad login)"
    assert not testLogin("JS","admin123456"), "Logged in to non-existing account (bad password)"
    print("Tests finished")

if __name__ == '__main__':
    tests()
