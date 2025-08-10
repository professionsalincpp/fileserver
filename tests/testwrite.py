import hashlib
import unittest
import requests
from serverurl import URL


class TestWrite(unittest.TestCase):
    def test_corrupt(self):
        response = requests.put(f"{URL}/api/write", json={
            "path": "corrupted.txt",
            "data": "corrupted", 
            "hash": "definetlynotavalidhash",
        })
        self.assertEqual(response.status_code, 400)

    def test_normal(self):
        response = requests.put(f"{URL}/api/write", json={
            "path": "not_corrupted.txt",
            "data": "not corrupted", 
            "hash": hashlib.sha256("not corrupted".encode("utf-8")).hexdigest(),
        })
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()