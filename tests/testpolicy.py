import hashlib
import unittest
import requests
from serverurl import URL


class TestPolicy(unittest.TestCase):
    def test_policy(self):
        for i in range(100):
            response = requests.put(f"{URL}/api/write", json={
                "path": f"../tests/lorem{i}.txt",
                "data": "not corrupted", 
                "hash": hashlib.sha256("not corrupted".encode("utf-8")).hexdigest(),
            })

if __name__ == '__main__':
    unittest.main()