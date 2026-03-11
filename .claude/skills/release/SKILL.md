---
name: release
description: Create a new SDK release — bump version, update HISTORY.md, commit, and tag
allowed-tools: Read, Bash, Edit, Write, Glob, Grep, Agent, WebFetch
---

# Create SDK Release

Bumps the SDK version, generates release notes in HISTORY.md, commits, and creates a git tag.

## Usage

- `/release patch` — bump patch version (e.g., 9.2.1 → 9.2.2)
- `/release minor` — bump minor version (e.g., 9.2.1 → 9.3.0)
- `/release major` — bump major version (e.g., 9.2.1 → 10.0.0)
- `/release 9.3.0` — set an explicit version

If no argument is provided, default to `patch`.

## Instructions

### 1. Determine the new version

Read the current version from `pyatlan/version.txt`. Parse the argument to compute the new version:

- `patch`: increment the third number, e.g., `9.2.1` → `9.2.2`
- `minor`: increment the second number, reset patch, e.g., `9.2.1` → `9.3.0`
- `major`: increment the first number, reset minor and patch, e.g., `9.2.1` → `10.0.0`
- If the argument matches a semver pattern (e.g., `9.3.0`), use it directly

Confirm the new version with the user before proceeding.

---

### 2. Gather changes since last release

Run:
```bash
git log --oneline $(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)..HEAD
```

If no tags exist, use all commits on the current branch. This gives you the list of changes to summarize.

Also check merged PRs for additional context:
```bash
gh pr list --state merged --base main --limit 30 --json title,labels,number,mergedAt
```

---

### 3. Draft release notes

Write the release notes following HISTORY.md conventions exactly:

**Header format:**
```
## X.Y.Z (Month Day, Year)
```

Use the current date. Month is full name, day has no leading zero.

**Section order** (only include sections that have content):

1. `### New Features` — new functionality
2. `### Breaking Changes` — breaking API changes
3. `### Experimental: pyatlan_v9` — v9-specific changes
4. `### Bug Fixes` — bug fixes
5. `### Packages` — dependency updates
6. `### QOL Improvements` — catch-all for misc improvements

**Formatting rules:**
- Use dashes (`-`) for bullet points
- Bold the key phrase at the start: `- **Short description**: Detailed explanation.`
- Be concise but thorough — describe what changed and why it matters
- Group related changes into single bullets where it makes sense

Present the draft to the user for review and iterate until approved.

---

### 4. Update version.txt

Write the new version number to `pyatlan/version.txt` (single line, no trailing newline beyond what was there).

---

### 5. Update HISTORY.md

Prepend the new release notes to the top of `HISTORY.md`, followed by a blank line before the previous release.

---

### 6. Commit and tag

```bash
git add pyatlan/version.txt HISTORY.md
git commit -m "[release] Bumped to release X.Y.Z"
git tag vX.Y.Z
```

The commit message must follow the exact pattern: `[release] Bumped to release X.Y.Z`

The tag must be `vX.Y.Z` (with the `v` prefix) — this is validated by `check_tag.py` during publishing.

---

### 7. Push

Ask the user before pushing. When confirmed:

```bash
git push && git push --tags
```

---

## Notes

- The version in `pyatlan/version.txt` is the single source of truth — `pyproject.toml` reads it dynamically
- The git tag must match the version (`vX.Y.Z` ↔ `X.Y.Z`) — enforced by `check_tag.py` in CI
- GitHub's `release.yml` auto-categorizes PRs by label into GitHub release notes, but `HISTORY.md` is the canonical changelog maintained manually
- After pushing the tag, a GitHub Release should be created (manually or via GitHub UI) to trigger the PyPI publish workflow
