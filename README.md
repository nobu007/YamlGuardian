# YamlGuardian
YamlGuardian

## Continuous Integration

This project uses GitHub Actions for continuous integration. The CI workflow is defined in the `.github/workflows/ci.yml` file. It runs tests on every push and pull request to ensure the codebase remains stable.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Poetry

### Installing Poetry

If you don't have Poetry installed, you can install it using the following command:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

### Setting Up the Project

1. Clone the repository:

```sh
git clone https://github.com/nobu007/YamlGuardian.git
cd YamlGuardian
```

2. Install the dependencies using Poetry:

```sh
poetry install
```

### Running Tests

You can run the tests using the following command:

```sh
poetry run python -m unittest discover -s tests
```

### Running Edge Case Tests

To run the edge case tests, use the following command:

```sh
poetry run python -m unittest tests/test_validate.py
```

### Analyzing Directory Structure

To analyze the directory structure and identify necessary changes, run the following script:

```sh
poetry run python yamlguardian/directory_analyzer.py
```

The identified changes will be saved in a CSV file named `directory_structure_changes.csv` in the root directory.

### Analyzing and Saving Directory Structure

To analyze the directory structure and save the changes to a CSV file, use the `analyze_and_save_directory_structure` method in `YamlGuardian`:

```python
from yamlguardian.core import YamlGuardian

guardian = YamlGuardian(schema_file='path/to/schema.yaml')
guardian.analyze_and_save_directory_structure(root_dir='path/to/root_dir', csv_file='path/to/output.csv')
```

## Design Documentation

For detailed design documentation, please refer to the [DESIGN.md](DESIGN.md) file.
