---
hide:
  - navigation
  - toc
---

<div align="center" markdown>

![pyatlan logo](https://github.com/user-attachments/assets/38243809-d723-4464-8f1c-4869795ea0c8){ width="260" }

# pyatlan

**The official Python SDK for [Atlan](https://atlan.com) :blue_heart:**

[![PyPI version](https://img.shields.io/pypi/v/pyatlan.svg)](https://pypi.org/project/pyatlan/)
[![Python versions](https://img.shields.io/pypi/pyversions/pyatlan.svg)](https://pypi.org/project/pyatlan/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Downloads](https://img.shields.io/pypi/dm/pyatlan.svg)](https://pypi.org/project/pyatlan/)
[![Build Status](https://github.com/atlanhq/atlan-python/actions/workflows/pyatlan-publish.yaml/badge.svg)](https://github.com/atlanhq/atlan-python/actions/workflows/pyatlan-publish.yaml)

[Get started](#installation){ .md-button .md-button--primary }
[API Reference](api/client.md){ .md-button }
[GitHub](https://github.com/atlanhq/atlan-python){ .md-button }

</div>

---

## Installation

=== "pip"

    ```bash
    pip install pyatlan
    ```

=== "uv"

    ```bash
    uv add pyatlan
    ```

=== "uv (dev)"

    ```bash
    git clone https://github.com/atlanhq/atlan-python.git
    cd atlan-python
    uv sync --group dev
    ```

---

## Quick Start

```python
from pyatlan.client import AtlanClient

# Initialize the client
client = AtlanClient(
    base_url="https://<your-tenant>.atlan.com",
    api_key="<your-api-key>",
)

# Search for assets
from pyatlan.model.fluent_search import FluentSearch
from pyatlan.model.assets import Table

response = client.asset.search(
    FluentSearch()
    .where(FluentSearch.asset_type(Table))
    .where(FluentSearch.active_assets())
    .page_size(10)
    .to_request()
)

for asset in response:
    print(asset.name, asset.qualified_name)
```

---

## Features

<div class="grid cards" markdown>

-   :material-magnify:{ .lg .middle } **Search & Discover**

    ---

    Full-text and structured search across all your data assets — tables, dashboards, glossary terms, and more.

-   :material-shield-check:{ .lg .middle } **Data Governance**

    ---

    Manage access control, business policies, data contracts, lineage, and custom metadata at scale.

-   :material-connection:{ .lg .middle } **260+ Asset Types**

    ---

    First-class support for Snowflake, Databricks, dbt, Tableau, Looker, PowerBI, Kafka, S3, and many more.

-   :material-lightning-bolt:{ .lg .middle } **Async Support**

    ---

    All client methods available in both sync and async flavors via `pyatlan.client.aio`.

-   :material-lock:{ .lg .middle } **Type Safe**

    ---

    Full `py.typed` marker, strict Pydantic v2 models, and comprehensive type stubs (`.pyi`).

-   :material-package-variant:{ .lg .middle } **Minimal Dependencies**

    ---

    Only what you need: `httpx`, `pydantic`, `authlib`, `msgspec`, and a few more.

</div>

---

## What's in this SDK?

| Module | Description |
|--------|-------------|
| [`AtlanClient`][pyatlan.client.atlan.AtlanClient] | Main entry point — all sub-clients live here |
| `pyatlan.model.assets` | 260+ asset model classes (Table, Column, Dashboard, …) |
| `pyatlan.model.search` | `IndexSearchRequest`, `Bool`, `Term`, and other DSL builders |
| `pyatlan.model.fluent_search` | Fluent builder API for composing searches |
| `pyatlan.cache` | In-memory caches for tags, metadata, groups, roles, users |
| `pyatlan.events` | Lambda / event-handler base classes |
| `pyatlan.model.typedef` | TypeDef management (custom metadata, enums, structs) |

---

## Project Stats

- :snake: **Python**: 3.9 · 3.10 · 3.11 · 3.12 · 3.13
- :package: **Stability**: Production-ready (`5 - Production/Stable`)
- :scales: **License**: Apache 2.0
- :rocket: **Async**: Native async/await support

---

## Contributing

```bash
# Fork & clone
git clone https://github.com/atlanhq/atlan-python.git
cd atlan-python

# Install dev dependencies
uv sync --group dev

# Run tests
uv run pytest tests/unit

# Run all QA checks (lint, type-check, format)
uv run ./qa-checks
```

See [CONTRIBUTING.md](https://github.com/atlanhq/atlan-python/blob/main/CONTRIBUTING.md) on GitHub.
