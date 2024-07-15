import unittest
from protocol import TCPR

class ProtocolTest(unittest.TestCase):
    def setUp(self):
        room_name = "hello"
        operation = 1
        state = 0
        user_name = "taichi"
        password = "Abcv123"

        self.protocol = TCPR.set_header(len(room_name), operation, state, len(user_name), room_name, user_name, password)

    def test_get_operation(self):
        operation = TCPR.get_operation(self.protocol)
        self.assertEqual(operation, 1)

    def test_get_state(self):
        state = TCPR.get_state(self.protocol)
        self.assertEqual(state, 0)

    def test_get_payload(self):
        payload = TCPR.get_payload(self.protocol)
        self.assertEqual(payload, ("hello", "taichi", "Abcv123"))


if __name__ == "__main__":
    unittest.main()

