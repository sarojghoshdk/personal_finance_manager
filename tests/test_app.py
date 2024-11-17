import unittest
from app import register_user, authenticate_user, add_transaction

class TestPersonalFinanceApp(unittest.TestCase):

    def test_registration(self):
        # Assume this test will register a new user successfully.
        register_user("testuser", "testpassword")
        self.assertIsNotNone(authenticate_user("testuser", "testpassword"))

    def test_add_transaction(self):
        # Assume user ID 1 is authenticated
        add_transaction(1, 500, "Food", "2024-11-08", "expense")

if __name__ == "__main__":
    unittest.main()

