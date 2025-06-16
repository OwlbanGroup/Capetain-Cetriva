import unittest


from integration_test_script import integration_test


class TestIntegration(unittest.TestCase):

    def test_integration_script_runs(self):
        try:
            integration_test()
        except Exception as e:
            self.fail(f"Integration test script raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
