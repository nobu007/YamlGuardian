# CORE_ARCHITECTURE.md

## 1. Overview

This document defines the core architectural concepts for the YamlGuardian project. In particular, it details the 3x3 matrix (hereafter referred to as the **Responsibility Definition Matrix**) used to clarify the responsibilities of each module.

## 2. Overall Architecture

The YamlGuardian architecture consists of the following three main elements:

1.  **Application Layer:**
    *   Defines the overall use cases of the system and handles external requests.
    *   Realizes use cases by coordinating the `Orchestration`, `Presentation`, and `Validation` modules.
    *   **Facade Pattern:** Each use case utilizes complex subsystems such as the `Validation` module concisely through the `Facade` pattern, reducing code complexity.
2.  **Responsibility Definition Matrix:**
    *   A 3x3 matrix for clarifying the responsibilities of each module.
    *   Consists of three axes: module type, processing direction, and processing stage.
    *   See "3. Responsibility Definition Matrix" for details.
3.  **Common Components:**
    *   Provides common functionality shared throughout the system.
    *   Includes logging, utility functions, and exception handling.

## 3. Responsibility Definition Matrix

In YamlGuardian, a matrix consisting of the following three axes is used to clarify the responsibilities of modules:

*   **Purpose:**
    *   Clarify the responsibilities of each module.
    *   Serve as a guideline for determining the location of code.
    *   Make the architecture easier for the entire team to understand.
*   **Reason for 3x3:**
    *   The YamlGuardian architecture is designed to maximize the separation of functions, ensuring that each module has a single responsibility.
    *   To achieve this goal, modules are finely classified along three axes—module type, processing direction, and processing stage—and the responsibilities of each module are clearly defined.

### 3.1 Module Type

The specific processing for each function varies depending on the module type.

1.  **Validation:**
    *   Includes `Schema`, `Rule`, and `Data` submodules.
2.  **Presentation:**
    *   Includes `Input` and `Output` submodules.

### 3.2 Processing Direction

Each process is defined as having one of the following directions. This direction can be identified by the naming convention of the submodules.

1.  **Interaction-Facing:**
    *   Deals with interactions with external systems or users.
    *   Submodules follow the naming convention `prepare -> transform -> deliver`.
2.  **Core-Facing:**
    *   Deals with processing related to the core logic of the application.
    *   Submodules follow the naming convention `input -> logic -> output`.

### 3.3 Processing Stage

In the YamlGuardian architecture, processing stages are divided into two types: "Interaction Processing Stage" and "Core Processing Stage."

1.  **Interaction Processing Stage:**
    *   **Target Module**: Presentation
    *   **Stages:**
        1.  **Prepare:** Receive data from the outside and convert it into a format that can be used internally by the system.
        2.  **Logic:** Validate and transform the received data into a format that is easy to process by subsequent modules.
        3.  **Postprocess:** Provide data processed internally by the system in a format that the next layer can use.

2.  **Core Processing Stage:**
    *   **Target Module**: Validation
    *   **Stages:**
        1.  **Extract:** Retrieve data from the information sources required for validation.
        2.  **Transform:** Transform the retrieved information into a format that the validation logic can use.
        3.  **Deliver:** Provide validation results and processed data to the outside as needed, or save them to a cache.

## 4. Submodule Naming Conventions

The naming conventions for submodules are fixed in the following two patterns. However, if these naming conventions are not suitable, consider a more appropriate name and clearly document the reason.

*   **Core-Facing (Logic-Side) Processing:** input -> logic -> output
*   **Interaction-Facing (User-Side) Processing:** prepare -> transform -> deliver

## 5. Other

*   **Common Components:**
    *   `Commons`: Provides logging, utility functions, etc.
    *   `Infrastructure`: Abstracts external service integrations, etc.
*   **Design Principles:**
    *   Actively utilize the Dependency Inversion Principle to increase flexibility and testability.
    *   Increase code reusability and improve maintainability by centralizing common processing in the `Commons` module.
    *   Increase system portability by reducing dependencies on external services and frameworks through the `Infrastructure` module.
    *   Improve code quality by clarifying the responsibilities of each module, making unit testing easier.
    *   The 3x3 matrix is merely a guideline for design and should be adapted flexibly according to the situation.

## 6. Purpose of the Matrix

*   Clarify the responsibilities of each module.
*   Serve as a guideline for determining the location of code.
*   Make the architecture easier for the entire team to understand.
</original_text>