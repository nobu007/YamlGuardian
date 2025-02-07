# YamlGuardian Design Document

## 1. System Objectives
YamlGuardian is a tool for validating data based on YAML files. This system is used to check whether data is correct according to defined rules, especially when validating forms or managing configurations. This ensures data integrity and accuracy, and promotes early detection of errors.

## 2. Features
### Main Features
#### YAML File Loading
Loads schema files, relation files, and common definition files to structure data.

#### Data Validation
Validates whether the specified data is correct based on the YAML schema.
Returns an error message if required fields are missing or rules are violated.

#### Rule Application
Performs appropriate validation according to conditions based on each rule.

### Additional Features
- Log output of validation results
- Detailed error tracing
- Provision of CLI interface

## 3. Architecture

### 3.0 Directory Structure

```
Directory structure:
└── YamlGuardian/
    ├── main.py
    ├── pyproject.toml
    ├── YamlGuardian/
    │   ├── core.py
    │   ├── rules.py
    │   └── validator.py
    ├── rule_config/
    │   ├── common_definitions/
    │   │   └── common_definitions.yaml
    │   └── page_definitions/
    │       ├── xxxx1/
    │       │   ├── yyyy1.yaml ...
    │       │   └── root_element_relations.yaml
    │       └── xxxx2/
    │           ├── yyyy2.yaml ...
    │           └── root_element_relations.yaml
    ├── schema/
    │   └── schema.yaml
    ├── test_yamls/
    ├── tests/
    │   └── rule_config/
    │       └── page_definitions/
    │           └── page1/
    │               ├── test_data.yaml
    │               ├── test_invalid_data.yaml
    │               └── test_schema.yaml
    ├── yamlguardian/
    │   ├── analyze_directory_structure.py
    │   ├── cerberus_adapter.py
    │   ├── cli.py
    │   ├── core.py
    │   ├── directory_analyzer.py
    │   ├── hierarchy_merger.py
    │   ├── hierarchy_reader.py
    │   ├── rules.py
    │   ├── validate.py
    │   └── validator.py
    └── .github/
        └── workflows/
            └── ci.yml
```

### 3.1 Module Configuration
- `core.py`: Provides the core functionality of YamlGuardian and manages YAML file loading and data validation.
- `validator.py`: Module for validating data based on YAML rules.
- `rules.py`: Module for managing rules and performing validation.
- `validate.py`: Module for validating YAML data.
- `directory_analyzer.py`: Module for analyzing directory structure and detecting changes.
- `hierarchy_reader.py`: Module for reading the hierarchical structure of YAML files.
- `hierarchy_merger.py`: Module for merging multiple hierarchical structures.
- `analyze_directory_structure.py`: Module for analyzing directory structure and detecting changes.
- `cerberus_adapter.py`: Module for converting YAML schema to Cerberus schema.
- `cli.py`: Module for providing a command-line interface.

### 3.2 Data Structure
#### Schema Structure
```yaml
root_element:
  - name: "FormA"
    type: "form"
    description: "このフォームはラベルとラジオボタンの関係を定義します。"
    attributes:
      action: "/submit"
      method: "post"
    elements:
      - name: AAA
        type: label
        required: true
        ...
```

#### Relation Structure
```yaml
root_element_relations:
  - source: "FormA"
    target: "FormB"
    condition: "exists"
```

#### Common Element Structure
```yaml
common_elements:
  - name: commonLabel
    type: label
    required: true
    ...
```

## 4. Data Flow
### YAML File Loading
The user provides the paths to the schema file, relation file, and common definition file to YamlGuardian.
YamlGuardian loads these files and creates a data structure.

### Data Validation
The user provides the data they want to validate.
YamlGuardian validates the data based on the loaded schema and relations.

### Error Reporting
If the validation result is an error, an error message is generated and returned to the user.

## 5. Error Handling
### Required Field Error
If a required field is missing, the message "フィールド名が存在しません。" is returned.

### Forbidden Field Error
If a forbidden field exists, the message "フィールド名は選択できません。" is returned.

### YAML Loading Error
If loading the YAML file fails, an appropriate error message is displayed.

## 6. Extensibility
### Adding New Rules
It is easy to add new rule-related functionality, and it can be extended by incorporating new validation logic into rules.py.

### Support for New YAML Formats
It is possible to extend the loading function to support additional YAML formats.

## 7. Future Prospects
### Addition of GUI Interface
We will consider developing a GUI so that users can validate data more intuitively.

### CI/CD Integration
We will continuously check data integrity by performing automated testing and integration.

## 8. Validation Stages
### Stage 1: Schema validation using `validate_openapi_schema`
In this stage, the input YAML data is validated against the OpenAPI schema to ensure it conforms to the defined structure and rules.

### Stage 2: User-defined YAML validation
In this stage, the input YAML data is validated against user-defined schemas to ensure it meets the specific requirements defined by the user.

### Stage 3: User-provided YAML validation
In this stage, the input YAML data is validated against the schemas provided by the user to ensure it adheres to the expected format and rules.

## 9. CLI Interface and Usage
The CLI interface is a tool for validating data from the command line. You can validate YAML data using the following command:

```sh
python -m yamlguardian.cli <data_file> <schema_file>
```

This command loads the specified data file and schema file and verifies whether the data conforms to the schema. The validation result is displayed as a success or error message.

## 10. FastAPI Server and Endpoints
The FastAPI server provides endpoints for receiving HTTP requests and validating data. The following is a description of the main endpoints.

### `/schema` Endpoint
This endpoint publishes the schema in JSON format. When a GET request is sent, the schema is returned.

### `/validate` Endpoint
This endpoint validates YAML data. When a POST request is sent and YAML data is included in the request body, the validation result is returned.

## 11. Directory Structure Analysis and Saving Changes to CSV File
Provides functionality to analyze directory structure and save changes to a CSV file. You can use the following command to analyze the directory structure and save the changes:

```sh
python -m yamlguardian.analyze_directory_structure <root_directory>
```

This command analyzes the specified root directory and saves the changes to the `directory_structure_changes.csv` file.

## 12. Implementation of Validation Stages
The `yamlguardian/validate.py` file implements the following validation stages:

### Stage 1: Schema validation using `validate_openapi_schema`
In this stage, the input YAML data is validated to ensure it conforms to the OpenAPI schema.

### Stage 2: User-defined YAML validation
In this stage, the input YAML data is validated to ensure it conforms to the user-defined schema.

### Stage 3: User-provided YAML validation
In this stage, the input YAML data is validated to ensure it conforms to the user-provided schema.

## 13. Future Prospects
### Addition of GUI Interface
We will consider developing a GUI so that users can validate data more intuitively.

### CI/CD Integration
We will continuously check data integrity by performing automated testing and integration.

## 14. Glossary

### OpenAPI Schema (openapi_schema)
A schema defined based on the OpenAPI specification. Represents the rules for yaml_validation_rules itself.

### Validation Rules (validation_rules)
YAML data entered based on openapi_schema. Provided in yaml file format.

### Validation Target (validation_target)
YAML data entered as a validation target.

### schema
A variable that stores the result of reading the validation rules.

### common_definitions
A variable that stores the result of reading the common definition file.

### rule_manager
An object for managing rules and performing validation.

### hierarchy_reader
An object for reading hierarchical structures.

### hierarchy_merger
An object for merging hierarchical structures.

### Validation Schema (validation_schema)
A variable that stores the validation rules after merging hierarchical structures.

### Validation Schema Cache (validation_schema_cache)
A variable that caches the validation rules after merging hierarchical structures.

### validation_schema_cache_file
A variable that stores the file path for saving the validation schema cache.

### analyzer
An object for performing directory analysis.

### root_directory
A variable that stores the path of the root directory to be analyzed.

### changes
A variable that stores a list of files and directories that have been changed as a result of directory analysis.

### changes_csv_file
A variable that stores the path of the CSV file to save the change results.
