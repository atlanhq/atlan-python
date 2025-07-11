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
   # Install dependencies using uv
   uv sync --extra dev
   ```

### Code Formatting
Before committing code, ensure it adheres to the repository's formatting guidelines. You can apply the required formatting using the below command:

```bash
uv run ./formatter
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
uv run ./qa-checks
```

### Running Unit Tests
You can run the SDK's unit tests **without needing access to an Atlan environment**:

```bash
uv run pytest tests/unit
```

### Running Integration Tests
Once the environment is set up, you can run integration tests:

- All integration tests:
  ```bash
  uv run pytest tests/integration
  ```
- Specific integration tests:
  ```bash
  uv run pytest tests/integration/<test_specific_feature>.py
  ```

## Docker

### Using Published Images

Pre-built Docker images are available from GitHub Container Registry:

```bash
# Latest version
docker pull ghcr.io/atlanhq/atlan-python:latest

# Specific version
docker pull ghcr.io/atlanhq/atlan-python:7.1.1
```

**Usage:**
```bash
# Interactive Python session
docker run -it --rm ghcr.io/atlanhq/atlan-python:latest

# Run a Python script
docker run -it --rm -v $(pwd):/app ghcr.io/atlanhq/atlan-python:latest python your_script.py

# With environment variables
docker run -it --rm \
  -e ATLAN_API_KEY=your_api_key \
  -e ATLAN_BASE_URL=https://your-tenant.atlan.com \
  ghcr.io/atlanhq/atlan-python:latest
```

### Building Locally

You can build the Docker image locally:

```bash
# Build the image
docker build -t pyatlan --build-arg VERSION=7.1.1 .

# Test the image
docker run -it --rm pyatlan python -c "import pyatlan; print('PyAtlan loaded successfully!')"
```

**Available images:**
- **Latest**: `ghcr.io/atlanhq/atlan-python:latest`
- **Versioned**: `ghcr.io/atlanhq/atlan-python:x.y.z`

### Running the SDK Model Generator

If you've pushed new typedefs to Atlan and want to generate SDK asset models to manage them via the SDK, this section covers how to run the SDK generator.

> [!NOTE]
> Before running any generator scripts, make sure you have [configured your environment variables](https://developer.atlan.com/sdks/python/#configure-the-sdk) specifically `ATLAN_BASE_URL` and `ATLAN_API_KEY`.

1. Run the combined generator script that handles all steps automatically:

   ```shell
   # Use default location (/tmp/typedefs.json)
   uv run ./generator

   # Or specify a custom typedefs file location
   uv run ./generator ./my-typedefs.json
   ```

   This script will:
   - Check if typedefs file exists and is current (skip if already created today)
   - Retrieve typedefs from your Atlan instance if needed
   - Generate the asset `models`, `enums`, and `struct` modules
   - Format the generated code automatically
   - Support custom typedefs file paths for flexibility

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
