import unittest
from yamlguardian.cerberus_adapter import convert_yaml_to_cerberus, load_yaml_file

class TestCerberusAdapter(unittest.TestCase):

    def test_convert_yaml_to_cerberus(self):
        yaml_schema = {
            'name': {'type': 'string', 'minlength': 1, 'maxlength': 50, 'required': True},
            'age': {'type': 'integer', 'min': 0, 'required': True}
        }
        cerberus_schema = convert_yaml_to_cerberus(yaml_schema)
        self.assertEqual(cerberus_schema['name']['type'], 'string')
        self.assertEqual(cerberus_schema['name']['minlength'], 1)
        self.assertEqual(cerberus_schema['name']['maxlength'], 50)
        self.assertEqual(cerberus_schema['name']['required'], True)
        self.assertEqual(cerberus_schema['age']['type'], 'integer')
        self.assertEqual(cerberus_schema['age']['min'], 0)
        self.assertEqual(cerberus_schema['age']['required'], True)

    def test_load_yaml_file(self):
        yaml_content = load_yaml_file('tests/test_schema.yaml')
        self.assertIsInstance(yaml_content, dict)

if __name__ == '__main__':
    unittest.main()
