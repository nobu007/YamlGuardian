# ARCHITECTURE.md

## 1. Overview

This document outlines the architecture of the YamlGuardian project, focusing on clear separation of concerns and a modular design. The system is designed to validate YAML data based on predefined rules and schemas. The architecture prioritizes testability, maintainability, and extensibility.

## 2. System Architecture

The architecture is based on a modified Clean Architecture, incorporating elements of Hexagonal Architecture to emphasize separation of concerns and dependency inversion.

```plaintext
YamlGuardian
├── Application     # Defines system-wide use cases
│   └── validation_usecase.py # YAML validation use case
├── Orchestration   # Orchestrates the processing of use cases
│   └── validation_orchestrator.py # YAML validation orchestrator
├── Validation      # Validation functionality
│   ├── __init__.py     # Package initialization
│   ├── validation_facade.py # Facade for validation processing
│   ├── Schema        # Management of schema definitions
│   │   ├── __init__.py  # Package initialization
│   │   ├── common      # Common schema processing, I/O independent
│   │   │   └── schema_utils.py # Schema manipulation utilities
│   │   │   └── schema_converter.py # Schema conversion
│   │   ├── input     # Receives schema information required for validation (logic side)
│   │   │   └── schema_loader.py # Schema loading
│   │   ├── logic   # Schema validation and manipulation (logic side)
│   │   │   └── schema_validator.py # Schema validation
│   │   │   └── schema_modifier.py # Schema manipulation (e.g., applying default values)
│   │   └── output    # Provides validated schema (logic side)
│   │   │   └── schema_cache.py # Schema cache
│   │   └── schema_definition.py # Schema definition (data class)
│   ├── Rule          # Validation rule management
│   │   ├── __init__.py  # Package initialization
│   │   ├── common      # Common rule processing, I/O independent
│   │   │   └── rule_utils.py # Rule manipulation utilities
│   │   ├── input     # Receives rule information required for validation (logic side)
│   │   │   └── rule_loader.py # Rule loading
│   │   ├── logic   # Rule validation and application (logic side)
│   │   │   └── rule_validator.py # Rule validation
│   │   │   └── rule_applier.py # Rule application
│   │   └── output    # Provides validated rules (logic side)
│   │   │   └── N/A
│   │   └── N/A
│   ├── Data          # Management of data to be validated
│   │   ├── __init__.py  # Package initialization
│   │   ├── common      # Common data processing, I/O independent
│   │   │   └── data_utils.py # Data manipulation utilities
│   │   ├── input     # Receives data required for validation (logic side)
│   │   │   └── data_loader.py # Data loading
│   │   ├── logic   # Data validation (logic side)
│   │   │   └── data_validator.py # Data validation
│   │   └── output    # Provides validation results (logic side)
│   │   │   └── result_formatter.py # Validation result formatting
├── Presentation    # External interface (CLI, API, presenter)
│   ├── Input          # Input processing
│   │   ├── __init__.py  # Package initialization
│   │   ├── common      # Common processing of input data
│   │   │   └── N/A
│   │   ├── prepare      # Receives and parses input data (interaction side)
│   │   │   └── cli_handler.py # Handles input from CLI
│   │   │   └── api_handler.py # Handles input from API
│   │   ├── logic       # Validates and transforms input data (interaction side)
│   │   │   └── input_validator.py # Input validation
│   │   └── postprocess  # Passes validated data to Application (interaction side)
│   │   │   └── input_transformer.py # Data transformation
│   ├── Output         # Output processing
│   │   ├── __init__.py  # Package initialization
│   │   ├── common      # Common processing of output data
│   │   │   └── N/A
│   │   ├── prepare      # Formats output data (interaction side)
│   │   │   └── cli_formatter.py # Formats output for CLI
│   │   │   └── api_formatter.py # Formats output for API
│   │   ├── logic       # Validates and transforms output data (interaction side)
│   │   │   └── output_validator.py # Output validation
│   │   └── postprocess  # Output processing (interaction side)
│   │   │   └── output_sender.py # Output sending
├── Commons         # Common components
│   ├── CrossCutting# Logging, security, exception handling
│   │   └── logger.py # Logging
│   │   └── exception_handler.py # Exception handling
│   ├── Utilities   # General utility classes
│   │   └── string_utils.py # String manipulation
│   │   └── file_utils.py # File manipulation
├── Infrastructure
│   ├── FrameworkAdapter # Abstraction of framework-specific processing
│   │   └── file_system.py # File system access
│   └── ExternalAdapter # Abstraction of external service integration
│   │   └── json_schema.py # JSON schema validation
```

## 3. Module Responsibilities

### 3.1 Application

- Defines the system's overall use cases and handles external requests.
- `validation_usecase.py`: Implements the YAML validation use case. The use case calls the validation process, formats the results, and provides them to the Presentation layer.

### 3.2 Orchestration

- Orchestrates the processing of specific use cases.
- `validation_orchestrator.py`: Implements the YAML validation orchestration. The orchestration calls the ValidationFacade and prepares the data to be passed to the Presentation layer.

### 3.3 Validation

This package contains all the functionality related to data validation. It performs core-oriented processing.

- **validation_facade.py**:

  - `ValidationFacade` class: Provides the entry point for the validation process.
  - Oversees schema loading, rule application, and data validation.
  - The `run` method summarizes all the steps required for validation and returns the result.

- **Schema**:

  - Manages schema definitions.
  - `schema_definition.py`:
    - `SchemaDefinition` class: Defines the data structure of the schema.
    - Holds the schema type, data, and source path.
  - `common`: Provides common schema processing, I/O independent processing.
    - `schema_utils.py`: Provides utility functions for schema manipulation.
    - Performs processing such as schema normalization and copying.
    - `schema_converter.py`: Provides functionality to convert schema formats (e.g., YAML -> JSON Schema).
  - `input`: Receives schema information required for validation (core-oriented).
    - `schema_loader.py`: Provides functionality to load schemas from YAML files, etc.
    - Loads schemas from the file system and converts them into internal data structures.
  - `logic`: Provides schema validation and manipulation processing (core-oriented).
    - `schema_validator.py`: Provides functionality to validate the structure and content of schemas.
    - Validates schemas according to defined rules.
    - `schema_modifier.py`: Provides functionality to modify schemas (e.g., applying default values).
  - `output`: Provides validated schemas (core-oriented).
    - `schema_cache.py`: Provides functionality to save validated schemas to a cache.

- **Rule**:

  - Manages validation rules.
  - `rule_utils.py`: Provides utility functions for rule manipulation.
  - `rule_loader.py`: Provides functionality to load rules from YAML files, etc.
  - `rule_validator.py`: Provides functionality to validate the syntax and semantics of rules.
  - `rule_applier.py`: Provides functionality to apply loaded rules to validate data.

- **Data**:
  - Manages the data to be validated.
  - `data_utils.py`: Provides utility functions for data manipulation.
  - `data_loader.py`: Provides functionality to load data to be validated from YAML files, etc.
  - `data_validator.py`: Provides functionality to validate data based on schemas and rules.
  - `result_formatter.py`: Provides functionality to format validation results into an easy-to-read format (e.g., text).

### 3.4 Presentation

Handles external interfaces such as CLI, API, and presentation logic. Performs interaction-oriented processing.

- **Input**:
  - `cli_handler.py`: Provides functionality to accept and process input from the CLI (interaction-oriented).
  - `api_handler.py`: Provides functionality to accept and process input from the API (interaction-oriented).
  - `input_validator.py`: Provides functionality to validate the format and content of input data (interaction-oriented).
  - `input_transformer.py`: Provides functionality to transform input data into a format that is easy for the UseCase to handle (interaction-oriented).
- **Output**:
  - `cli_formatter.py`: Provides functionality to format validation results for the CLI (interaction-oriented).
  - `api_formatter.py`: Provides functionality to format validation results for the API (interaction-oriented).
  - `output_validator.py`: Provides functionality to validate the format and content of output data (interaction-oriented).
  - `output_sender.py`: Provides functionality to send validation results externally (interaction-oriented).

### 3.5 Common Components

Contains components shared throughout the system.

- `logger.py`: Provides logging functionality.
- `exception_handler.py`: Provides exception handling functionality.
- `string_utils.py`: Provides utility functions for string manipulation.
- `file_utils.py`: Provides utility functions for file manipulation.

### 3.6 Infrastructure

Provides an abstraction layer for external dependencies.

- `file_system.py`: Provides functionality to abstract file system access.
- `json_schema.py`: Provides functionality to abstract JSON Schema validation.
