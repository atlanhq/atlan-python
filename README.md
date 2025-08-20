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

- 🐍 **Python Versions**: 3.9, 3.10, 3.11, 3.12, 3.13
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
uv sync --group dev

# Run quality checks
uv run ./qa-checks

# Run tests
uv run pytest tests/unit
```

### Dependency Groups

This project uses uv dependency groups for better dependency management:

- **Core dependencies**: Always installed (`uv sync`)
- **Development dependencies**: Testing, linting, formatting (`uv sync --group dev`)
- **Documentation dependencies**: Sphinx docs (`uv sync --group docs`)

You can install multiple groups:
```bash
# Install both dev and docs dependencies
uv sync --group dev --group docs

# Install all dependencies
uv sync --all-groups
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
uv sync --group dev

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

## 📁 Project Structure

Understanding the codebase layout will help you navigate and contribute effectively:

```
atlan-python/
├── pyatlan/                          # 🐍 Main Python package
│   ├── __init__.py                   # Package initialization
│   ├── cache/                        # 💾 Caching mechanisms
│   │   ├── atlan_tag_cache.py       # Tag name ↔ GUID mapping
│   │   ├── custom_metadata_cache.py  # Custom metadata definitions
│   │   ├── enum_cache.py            # Enum value caching
│   │   └── aio/                     # Async versions of caches
│   ├── client/                       # 🌐 HTTP client implementations
│   │   ├── atlan.py                 # Main synchronous client
│   │   ├── asset.py                 # Asset operations (CRUD, search)
│   │   ├── admin.py                 # Administrative operations
│   │   ├── audit.py                 # Audit log operations
│   │   ├── common/                  # Shared client logic
│   │   └── aio/                     # Async client implementations
│   ├── model/                        # 📊 Data models and assets
│   │   ├── assets/                  # Asset type definitions
│   │   │   ├── core/                # Core asset types (Table, Database, etc.)
│   │   │   └── relations/           # Relationship models
│   │   ├── fields/                  # Search field definitions
│   │   ├── open_lineage/            # OpenLineage specification models
│   │   ├── packages/                # Package/workflow models
│   │   └── aio/                     # Async model variants
│   ├── generator/                    # 🏗️ Code generation tools
│   │   ├── templates/               # Jinja2 templates for generation
│   │   └── class_generator.py       # Main generation logic
│   ├── pkg/                         # 📦 Package creation utilities
│   ├── events/                      # 🔔 Event handling (webhooks, lambdas)
│   ├── samples/                     # 💡 Example code and scripts
│   └── test_utils/                  # 🧪 Testing utilities
├── tests/                            # 🧪 Test suite
│   ├── unit/                        # Unit tests (fast, no external deps)
│   ├── integration/                 # Integration tests (require Atlan instance)
│   └── data/                        # Test fixtures and mock data
├── docs/                            # 📚 Sphinx documentation
│   ├── conf.py                      # Sphinx configuration
│   └── *.rst                       # Documentation source files
├── pyproject.toml                   # 📋 Project configuration (deps, tools)
├── uv.lock                          # 🔒 Locked dependencies
├── qa-checks                        # ✅ Quality assurance script
├── formatter                        # 🎨 Code formatting script
└── generator                        # 🏗️ Model generation script
```

### Key Components

#### 🌐 **Client Layer** (`pyatlan/client/`)
- **Synchronous**: Direct HTTP operations using `httpx`
- **Asynchronous**: Async/await operations using `httpx.AsyncClient`
- **Common**: Shared business logic between sync/async clients
- **Specialized**: Domain-specific clients (admin, audit, lineage, etc.)

#### 📊 **Model Layer** (`pyatlan/model/`)
- **Assets**: 400+ asset types (tables, dashboards, pipelines, etc.)
- **Core Models**: Base classes, requests, responses
- **Fields**: Search and filtering field definitions
- **OpenLineage**: Data lineage specification compliance

#### 💾 **Cache Layer** (`pyatlan/cache/`)
- **Tag Cache**: Maps human-readable tag names to internal GUIDs
- **Custom Metadata**: Caches custom attribute definitions
- **Connection Cache**: Stores connector and connection metadata
- **Async Variants**: Full async implementations for all caches

#### 🏗️ **Generation System** (`pyatlan/generator/`)
- **Templates**: Jinja2 templates for assets, enums, documentation
- **Generator**: Retrieves typedefs and generates Python models
- **Incremental**: Only regenerates changed models for efficiency

#### 🧪 **Testing Strategy**
- **Unit Tests**: Fast, isolated tests with mocks/fixtures
- **Integration Tests**: Real API calls (requires credentials)
- **VCR Cassettes**: Record/replay HTTP interactions for consistent testing

#### 📦 **Package System** (`pyatlan/pkg/`)
- **Custom Packages**: Framework for building Atlan-deployable packages
- **Templates**: Pre-built package structures and configurations
- **Utilities**: Helper functions for package development

### Development Workflow

1. **Models**: Generated from your Atlan instance's typedefs
2. **Clients**: Hand-crafted for optimal developer experience  
3. **Tests**: Mix of unit (fast iteration) and integration (real validation)
4. **Quality**: Automated formatting, linting, and type checking
5. **Documentation**: Auto-generated from docstrings and examples

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
