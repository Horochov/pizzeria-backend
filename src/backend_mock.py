import requests
from backend import *
from unittest.mock import MagicMock
import unittest
import multiprocessing

def startBackend(mocked = False, port=5000):
    bend = Backend()
    if(mocked):
        bend.repo.login = MagicMock(return_value=True)
        menu = [
            [1,'name',9,99,'Pizza',1.23,'mm','brak'],
            [2,'żarówka',-1,65536,'wolfram, krzem',-1.0,'świeca międzynarodowa','Woda']]
        bend.repo.get_products = MagicMock(return_value=menu)
    
    bend.main(port)
    

if __name__ == '__main__':
    bck = startBackend(mocked=True)
    
