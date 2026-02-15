import unittest

from ry_firebase_sync import FirebaseRedisClient


class BasicTest(unittest.TestCase):
    def test_export(self) -> None:
        self.assertIsNotNone(FirebaseRedisClient)
