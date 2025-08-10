import hashlib
import unittest
import requests
from serverurl import URL


class TestRead(unittest.TestCase):
    def test_hash(self):
        response = requests.post(f"{URL}/api/read", json={"path": "tests/lorem.txt"})
        if response.status_code == 200:
            self.assertEqual(hashlib.sha256(response.json()["data"]["data"].encode("utf-8")).hexdigest(), response.json()["data"]["hash"])

    def test_not_found(self):
        response = requests.post(f"{URL}/api/read", json={"path": "notfound__P1234567bem.txt"})
        self.assertEqual(response.status_code, 404)
        
if __name__ == '__main__':
    unittest.main()