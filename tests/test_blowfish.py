import unittest
from datetime import date, timedelta
from Crypto.Cipher import Blowfish


class TestingTestCase(unittest.TestCase):
    def test_blowfish(self):
        cipher = Blowfish.new(b"test", mode=Blowfish.MODE_ECB)
        res = cipher.encrypt("abcdefgh".encode("utf-8"))
        out = cipher.decrypt(res).decode("utf-8")
        assert out == "abcdefgh"
