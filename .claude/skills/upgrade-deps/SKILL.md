---
name: upgrade-deps
description: Upgrade all pyatlan Python dependencies and GitHub Actions to their latest compatible versions
disable-model-invocation: true
allowed-tools: Read, Bash, Edit, Write, Glob, Grep, WebFetch
---

Upgrade all dependencies for the pyatlan Python SDK. Follow these steps carefully.

## Context

- The project supports Python >=3.9, so skip any package version that requires Python >=3.10 or higher
- Use `uv` for all Python package operations
- Workflow files are in `.github/workflows/`
- Dependencies are managed in `pyproject.toml` and locked in `uv.lock`

---

## Step 1 — Find outdated Python packages

Run:
```
uv pip list --outdated
```

Cross-reference the output with the direct dependencies pinned in `pyproject.toml` (sections: `dependencies`, `dev`, `docs`). Ignore transitive dependencies — only update packages that are explicitly listed in `pyproject.toml`.

---

## Step 2 — Check Python version compatibility for each outdated package

For every package identified in Step 1, check its `requires_python` field:

```
curl -s https://pypi.org/pypi/<package>/<new-version>/json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['info']['requires_python'])"
```

**Rules:**
- If `requires_python` is `>=3.9` or lower (or None) → safe to upgrade
- If `requires_python` is `>=3.10` or higher → check if an older compatible version exists:
  ```
  curl -s https://pypi.org/pypi/<package>/json | python3 -c "
  import json, sys
  d = json.load(sys.stdin)
  for v in sorted(d['releases'].keys(), reverse=True)[:10]:
      rels = d['releases'][v]
      if rels:
          rp = rels[0].get('requires_python','')
          print(f'{v}: {rp}')
  "
  ```
  Pick the highest version that supports Python 3.9. If already at that version, skip it.
- Packages already conditioned in pyproject.toml with `; python_version >= '3.10'` (like `filelock`) can be upgraded freely since they only install on 3.10+

---

## Step 3 — Update pyproject.toml

For each package that can be safely upgraded, update its version pin in `pyproject.toml`.

Keep the same `~=X.Y.Z` pinning style as used by other packages in the file.

---

## Step 4 — Upgrade GitHub Actions

Scan all workflow files in `.github/workflows/` for `uses:` lines:
```
grep -rh "uses:" .github/workflows/ | sort -u
```

For each action that uses a version tag, check the latest release:
```
curl -s https://api.github.com/repos/<owner>/<repo>/releases/latest | python3 -c "import json,sys; print(json.load(sys.stdin)['tag_name'])"
```

Use the major version tag style (e.g., `v7`) if the action uses that convention, or the exact version if it was pinned exactly (e.g., `0.34.2`).

Update all workflow files using sed in-place replacements for each changed action.

---

## Step 5 — Update pre-commit ruff rev

If ruff was upgraded in pyproject.toml, also update the `rev:` in `.pre-commit-config.yaml` to match:
```yaml
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v<new-version>
```

---

## Step 6 — Regenerate the lockfile

```
uv lock --upgrade
```

If this fails due to a Python version conflict, revisit Step 2 for the failing package.

---

## Step 7 — Install and run tests

```
uv sync --all-groups
python -m pytest tests/unit/ -x -q --tb=short
```

Fix any test failures caused by the upgrades before proceeding.

---

## Step 8 — Run pre-commit

```
pre-commit run --all-files
```

The first run may auto-fix formatting. Run again to confirm all hooks pass.

---

## Step 9 — Summarise and commit

Present a summary table of all changes made:

| Package / Action | Before | After | Notes |
|---|---|---|---|
| pydantic | 2.12.4 | 2.12.5 | |
| ... | | | |
| docker/login-action | v3 | v4 | |

Then commit:
```
git add pyproject.toml uv.lock requirements.txt .pre-commit-config.yaml .github/workflows/
git commit -m "chore: upgrade Python dependencies and GitHub Actions to latest versions"
```

Ask the user before pushing.
