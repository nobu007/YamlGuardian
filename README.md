# YamlGuardian
YamlGuardian

## Continuous Integration

This project uses GitHub Actions for continuous integration. The CI workflow is defined in the `.github/workflows/ci.yml` file. It runs tests on every push and pull request to ensure the codebase remains stable.

## Auto-Merge Feature

We have added a new auto-merge feature to our CI workflow. This feature automatically merges pull requests if all CI checks pass. The auto-merge process is handled by the `peter-evans/merge` GitHub Action. This ensures that only PRs that pass all checks are merged, maintaining the stability of the codebase.

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

### Running the FastAPI Server

To run the FastAPI server using `uvicorn`, use the following command:

```sh
uvicorn main:app --reload
```

### Validating YAML Data

To validate YAML data using the `/validate` endpoint, send a POST request to `http://127.0.0.1:8000/validate` with the YAML content in the request body. For example:

```sh
curl -X POST "http://127.0.0.1:8000/validate" -H "Content-Type: application/json" -d '{"yaml_content": "name: John\nage: 30"}'
```

## Fixing CI Errors

If you encounter CI errors, follow these steps to resolve them:

1. **Check the CI logs**: Review the logs in the GitHub Actions tab to identify the cause of the error.
2. **Common issues**:
   - **Dependency issues**: Ensure all dependencies are correctly specified in `pyproject.toml` and run `poetry install` to install them.
   - **Test failures**: Run the tests locally using `poetry run python -m unittest discover -s tests` to identify and fix any failing tests.
   - **Linting errors**: Ensure your code adheres to the project's linting rules. Run `poetry run flake8` to check for linting errors and fix them accordingly.
3. **Re-run the CI workflow**: After fixing the issues, push your changes to trigger the CI workflow again.

## Design Documentation

For detailed design documentation, please refer to the [DESIGN.md](DESIGN.md) file.
