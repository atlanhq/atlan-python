<div align="center">

<img src="https://github.com/user-attachments/assets/38243809-d723-4464-8f1c-4869795ea0c8" alt="pyatlan Logo" width="300">

**The official Python SDK for the Atlan 💙**

[![PyPI version](https://img.shields.io/pypi/v/pyatlan.svg)](https://pypi.org/project/pyatlan/)
[![Python versions](https://img.shields.io/pypi/pyversions/pyatlan.svg)](https://pypi.org/project/pyatlan/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Downloads](https://img.shields.io/pypi/dm/pyatlan.svg)](https://pypi.org/project/pyatlan/)
[![Build Status](https://github.com/atlanhq/atlan-python/actions/workflows/pyatlan-publish.yaml/badge.svg)](https://github.com/atlanhq/atlan-python/actions/workflows/pyatlan-publish.yaml)
[![Documentation](https://img.shields.io/badge/docs-developer.atlan.com-blue.svg)](https://developer.atlan.com/getting-started/python-sdk/)
[![Docker](https://img.shields.io/badge/docker-ghcr.io%2Fatlanhq%2Fatlan--python-blue.svg)](https://github.com/atlanhq/atlan-python/pkgs/container/atlan-python)

---

[**📖 Documentation**](https://developer.atlan.com/getting-started/python-sdk/) •
[**🐳 Docker**](#-docker) •
[**🤝 Contributing**](#-contributing)

</div>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## 📊 Project Stats

- 🐍 **Python Versions**: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- 📦 **Package Size**: Optimized for fast installation
- 🚀 **Performance**: Built with modern async/await support
- 🔧 **Dependencies**: Minimal, modern stack
- 📈 **Stability**: Production-ready

## 📦 Installation

### Production Use

```bash
# Latest stable version
pip install pyatlan

# Specific version
pip install pyatlan==7.1.3

# With uv (faster) - install uv first: curl -LsSf https://astral.sh/uv/install.sh | sh
uv add pyatlan
```

### Development Setup

```bash
# Clone the repository
git clone https://github.com/atlanhq/atlan-python.git
cd atlan-python

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install with development dependencies
uv sync --extra dev

# Run quality checks
uv run ./qa-checks

# Run tests
uv run pytest tests/unit
```

## 🐳 Docker

### Pre-built Images


```bash
# Latest version
docker pull ghcr.io/atlanhq/atlan-python:latest

# Specific version
docker pull ghcr.io/atlanhq/atlan-python:7.1.3
```

### Usage

```bash
# Interactive Python session
docker run -it --rm ghcr.io/atlanhq/atlan-python:latest

# Run a script
docker run -it --rm \
  -v $(pwd):/app \
  -e ATLAN_API_KEY=your_key \
  -e ATLAN_BASE_URL=https://your-tenant.atlan.com \
  ghcr.io/atlanhq/atlan-python:latest \
  python your_script.py
```

## 🧪 Testing

### Unit Tests
```bash
# Run all unit tests
uv run pytest tests/unit

# Run with coverage
uv run pytest tests/unit --cov=pyatlan --cov-report=html
```

### Integration Tests
```bash
# Set up environment
cp .env.example .env
# Edit .env with your Atlan credentials

# Run integration tests
uv run pytest tests/integration
```

### Quality Assurance
```bash
# Run all QA checks (formatting, linting, type checking)
uv run ./qa-checks

# Individual checks
uv run ruff format .          # Code formatting
uv run ruff check .           # Linting
uv run mypy .                 # Type checking
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/your-username/atlan-python.git
cd atlan-python

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install development dependencies
uv sync --extra dev

# Install pre-commit hooks
uv run pre-commit install
```

### Making Changes

```bash
# Create a feature branch
git checkout -b feature/amazing-feature

# Make your changes and test
uv run ./formatter
uv run ./qa-checks
uv run pytest tests/unit

# Commit with conventional commits
git commit -m "feat: add amazing feature"

# Push and create a pull request
git push origin feature/amazing-feature
```

### Guidelines

- ✅ Follow [conventional commits](https://www.conventionalcommits.org/)
- ✅ Add tests for new features
- ✅ Update documentation as needed
- ✅ Ensure all QA checks pass

## 🛠️ SDK Generator

Generate asset models from your Atlan instance:

```bash
# Generate models automatically
uv run ./generator

# Use custom typedefs file
uv run ./generator ./my-typedefs.json
```

This will:
- 📥 Retrieve typedefs from your Atlan instance
- 🏗️ Generate asset models, enums, and structures
- 🎨 Format code automatically
- ⚡ Support incremental updates

## 📄 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

## 🙏 Attribution

Portions of this SDK are based on original work from:
- **[Apache Atlas](https://github.com/apache/atlas)** (Apache-2.0 license)
- **[Elasticsearch DSL](https://github.com/elastic/elasticsearch-dsl-py)** (Apache-2.0 license)

<div align="center">

**Built with 💙 by [Atlan](https://atlan.com)**

[Website](https://atlan.com) • [Documentation](https://developer.atlan.com) • [Support](mailto:support@atlan.com)

</div>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)
