import unittest
import subprocess
import os

class TestCLI(unittest.TestCase):

    def test_cli_success(self):
        result = subprocess.run(['python', '-m', 'yamlguardian.cli', 'tests/test_data.yaml', 'tests/test_schema.yaml'], capture_output=True, text=True)
        self.assertIn("Validation succeeded.", result.stdout)

    def test_cli_failure(self):
        result = subprocess.run(['python', '-m', 'yamlguardian.cli', 'tests/test_invalid_data.yaml', 'tests/test_schema.yaml'], capture_output=True, text=True)
        self.assertIn("Validation failed with the following errors:", result.stdout)

if __name__ == '__main__':
    unittest.main()
