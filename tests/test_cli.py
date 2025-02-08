import subprocess
import unittest


class TestCLISuccess(unittest.TestCase):
    def test_cli_success(self):
        result = subprocess.run(
            [
                "python",
                "-m",
                "yamlguardian.cli",
                "tests/rule_config/page_definitions/page1/test_data.yaml",
                "tests/rule_config/page_definitions/page1/test_schema.yaml",
            ],
            capture_output=True,
            text=True,
        )
        assert "Validation succeeded." in result.stdout


class TestCLIFailure(unittest.TestCase):
    def test_cli_failure(self):
        result = subprocess.run(
            [
                "python",
                "-m",
                "yamlguardian.cli",
                "tests/rule_config/page_definitions/page1/test_invalid_data.yaml",
                "tests/rule_config/page_definitions/page1/test_schema.yaml",
            ],
            capture_output=True,
            text=True,
        )
        assert "Validation failed with the following errors:" in result.stdout


if __name__ == "__main__":
    unittest.main()
