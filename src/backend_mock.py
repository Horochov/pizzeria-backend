import requests
from backend import *
from unittest.mock import MagicMock
import unittest
import multiprocessing

def startBackend(mocked = False, port=5000):
    bend = Backend()
    if(mocked):
        bend.repo.login = MagicMock(return_value=True)
        bend.repo.get_products = MagicMock(return_value=True)
    
    bend.main(port)
    

if __name__ == '__main__':
    bck = startBackend(mocked=True)
    
