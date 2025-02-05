# ARCHITECTURE.md

## 1. Overview

This document outlines the architecture of the YamlGuardian project, focusing on a clear separation of concerns and modular design. The system is designed to validate YAML data against predefined rules and schemas. This architecture prioritizes testability, maintainability, and extensibility.

## 2. System Architecture

The architecture is based on a modified Clean Architecture, incorporating elements of Hexagonal Architecture to emphasize the separation of concerns and dependency inversion.

```plaintext
YamlGuardian
├── Orchestration # System-wide orchestration layer
├── Validation # Validation functionality
│ ├── Schema # Schema definition management
│ │ ├── common # Common schema handling, I/O independent
│ │ ├── prepare # Schema loading, parsing, pre-validation
│ │ ├── logic # Schema validation, manipulation
│ │ └── postprocess # Schema post-processing, caching, conversion
│ ├── Rule # Validation rule management
│ │ ├── common # Common rule handling, I/O independent
│ │ ├── prepare # Rule loading, parsing, pre-validation
│ │ ├── logic # Rule validation, application
│ │ └── postprocess # Rule post-processing, caching
│ ├── Data # Validation target data management
│ │ ├── common # Common data handling, I/O independent
│ │ ├── prepare # Data loading, transformation
│ │ ├── logic # Data validation based on schema and rules
│ │ └── postprocess # Data post-processing, error message generation
├── Presentation # External interface (CLI, API, Presenter)
│ ├── Input # Input processing
│ │ ├── common # Common input data handling
│ │ ├── prepare # Input data acceptance, parsing
│ │ ├── logic # Input data validation, transformation
│ │ └── postprocess # Passing validated data to UseCases
│ ├── Output # Output processing
│ │ ├── common # Common output data handling
│ │ ├── prepare # Output data formatting
│ │ ├── logic # Output data validation, transformation
│ │ └── postprocess # Output delivery
├── Commons # Common components
│ ├── CrossCutting# Logging, security, exception handling
│ ├── Utilities # Generic utility classes
├── Infrastructure
│ ├── FrameworkAdapter # Abstraction of framework-specific operations
│ └── ExternalAdapter # Abstraction of external service integrations
```

## 3. Module Responsibilities

### 3.1 Orchestration

- Responsible for orchestrating the entire validation process, coordinating interactions between different components.
- Acts as a facade, providing a single entry point for clients.

### 3.2 Validation

This package contains all functionalities related to data validation.

- **Schema**:
  - Manages schema definitions.
  - `common`: Handles schema loading and saving (I/O independent).
  - `prepare`: Parses YAML schema files and performs pre-validation.
  - `logic`: Validates and manipulates schema structures.
  - `postprocess`: Converts schemas to other formats (e.g., JSON Schema) and stores them in a cache.
- **Rule**:
  - Manages validation rules.
  - `common`: Handles rule loading and saving (I/O independent).
  - `prepare`: Parses YAML rule files and performs pre-validation.
  - `logic`: Applies and validates rules.
  - `postprocess`: Stores validated rules in a cache.
- **Data**:
  - Manages data to be validated.
  - `common`: Handles common data operations like loading and saving (I/O independent).
  - `prepare`: Loads and transforms data.
  - `logic`: Validates data based on schema and rules.
  - `postprocess`: Generates error messages and other validation-related tasks.

### 3.3 Presentation

Handles external interfaces such as CLI, API, and presentation logic.

- **Input**:
  - `common`: Handles general operations on incoming data.
  - `prepare`: Handles parsing of input from external sources.
  - `logic`: Validates and transforms the input data.
  - `postprocess`: Passes validated data to UseCases.
- **Output**:
  - `common`: General output handling.
  - `prepare`: Formats data for output.
  - `logic`: Validates and transforms the data before output.
  - `postprocess`: Delivers the output to the external interface.

### 3.4 Commons

Contains components that are shared across the entire system.

- **CrossCutting**:
  - Implements cross-cutting concerns such as logging, security, and exception handling.
- **Utilities**:
  - Provides generic utility classes such as string manipulation and date formatting.

### 3.5 Infrastructure

Provides abstraction layers for external dependencies.

- **FrameworkAdapter**:
  - Provides a wrapper around framework-specific operations, such as file system access and HTTP requests.
- **ExternalAdapter**:
  - Provides a wrapper around external service integrations such as database access and API calls.

## 4. Data Flow

1.  The Orchestration layer receives a request from the Presentation layer.
2.  The Orchestration layer coordinates with the Validation layer to validate the data.
3.  The Validation layer uses the Schema, Rule, and Data sub-components to perform the validation.
4.  The Infrastructure layer provides access to external resources such as file systems and databases.
5.  The Commons layer provides general-purpose utility functions and cross-cutting concerns such as logging.
6.  The Orchestration layer returns the validation results to the Presentation layer.
7.  The Presentation layer formats the results and displays them to the user.
