<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright 2022 Atlan Pte. Ltd. -->

[![SphinxDocs](https://img.shields.io/badge/sphinx--docs-passing-success)](https://atlanhq.github.io/atlan-python/)

# Atlan Python SDK

This repository houses the code for a Python SDK to interact with [Atlan](https://atlan.com).

## [Documentation](https://developer.atlan.com/getting-started/python-sdk/)

[https://developer.atlan.com/getting-started/python-sdk/](https://developer.atlan.com/getting-started/python-sdk/)



## Installing for Development

### Initial Setup
To get started developing the SDK:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Ensure you have Python 3.8 or later installed. You can verify your Python version with:
   ```bash
   python --version
   ```
   or
   ```bash
   python3 --version
   ```

3. Set up a virtual environment for development:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

4. Install the required dependencies:
   ```bash
   # Upgrade pip before installing dependencies
   python -m pip install --upgrade pip
   # Install required dependencies for development
   pip install -e . && pip install -r requirements-dev.txt  
   ```

### Code Formatting
Before committing code, ensure it adheres to the repository's formatting guidelines. You can apply the required formatting using the below command:

```bash
./pyatlan-formatter
```

### Environment Setup
For running integration tests, you'll need to configure your environment:

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Update the `.env` file with your Atlan API key and base URL.
3. Load the environment variables:
    - For macOS/Linux:
      ```bash
      export $(cat .env | xargs)
      ```
    - For Windows (PowerShell): Load environment variables
      ```powershell
      # Run this in PowerShell (not Command Prompt)   
      Get-Content .env | ForEach-Object {  
       if ($_ -match '^(.*?)=(.*)$') {  
        $env:($matches[1]) = $matches[2]  
       }  
      }
      ```
    - For macOS/Linux: Load environment variables from .env file
      ```bash
      export $(cat .env | xargs)
      ```


## Testing the SDK

### Run all the QA checks
You can run all the QA checks using the following command:

```bash
./qa-checks
```

### Running Unit Tests
You can run the SDK's unit tests **without needing access to an Atlan environment**:

```bash
pytest tests/unit
```

### Running Integration Tests
Once the environment is set up, you can run integration tests:

- All integration tests:
  ```bash
  pytest tests/integration
  ```
- Specific integration tests:
  ```bash
  pytest tests/integration/<test_specific_feature>.py
  ```

## Attribution

Portions of the SDK are based on original work from https://github.com/apache/atlas. Those classes that derive from this original work have an extra heading comment as follows:

```python
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)
```

Portions of the SDK are based on original work from https://github.com/elastic/elasticsearch-dsl-py. Those classes that derive from this original work have an extra heading comment as follows:

```python
# Based on original code from https://github.com/elastic/elasticsearch-dsl-py.git (under Apache-2.0 license)
```
----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright 2022 Atlan Pte. Ltd.
