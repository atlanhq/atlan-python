---
description: Generate pyatlan_v9 msgspec model files by cloning the models repo and running the Pkl code generator
---

# Generate v9 Models

Generates pyatlan_v9 msgspec model files from Pkl type definitions in the atlanhq/models repo.

## Usage

- `/generate-v9-models` — Clone models@BLDX-708, generate and sync v9 models
- `/generate-v9-models <branch>` — Clone models@<branch> instead
- `/generate-v9-models <branch> test` — Also run tests after sync
- `/generate-v9-models test` — Clone models@BLDX-708 and run tests after sync

## IMPORTANT: which branch and why

Generate from **`BLDX-708`** (models PR #1899), **not** `master`. Only BLDX-708's
`PythonMsgspecRenderer.pkl` emits the per-asset `validate()` / `minimize()` /
`relate()` methods. Generating from `master` silently drops those three methods
from every generated asset (~470 of them). `tests_v9/unit/model/asset_methods_test.py`
is a regression guard for exactly this.

Keep BLDX-708 rebased on `master` so the typedefs stay current — check with
`git merge-base --is-ancestor origin/master BLDX-708`. If BLDX-708 is a few
commits behind, review `git diff BLDX-708...origin/master` and port anything
material (e.g. the `Entity.custom_attributes` permissive-typing renderer fix,
which lands in the hand-managed `entity.py` — see step 4).

## Instructions

### 1. Clone or check out the models repo

```bash
SDK_DIR="$(pwd)"  # atlan-python root
MODELS_DIR="$(cd .. && pwd)/models"
BRANCH="BLDX-708"  # override with first non-"test" arg

if [ -d "$MODELS_DIR" ]; then
  cd "$MODELS_DIR" && git fetch origin && git checkout "$BRANCH" && git pull origin "$BRANCH"
else
  git clone git@github.com:atlanhq/models.git "$MODELS_DIR" && cd "$MODELS_DIR" && git checkout "$BRANCH"
fi
```

**Required generator fix on BLDX-708.** `ModelRenderer.getTypeNameFromMapping`
must use `.findOrNull(...)` (not `.find(...)`) in both the `customAssetTypes` and
`legacyAssetTypes` lookups. `.find` throws `Cannot find matching element in
collection` on any unresolved supertype and aborts the whole eval (only ~320 of
~670 files get written). `master` already uses `.findOrNull`; BLDX-708 regressed
it. Verify before generating:
```bash
grep -c "findOrNull((entry) -> entry.value == customType)" toolkit/src/main/pkl/ModelRenderer.pkl  # expect 2
```
This fix belongs upstream in models#1899.

### 2. Run Pkl evaluation

Use **pkl 0.27.0** (the version the workflow pins). Newer pkl (0.29.x) is not
required but the workflow is validated on 0.27.0. BLDX-708 uses a **boolean**
`sdkOnly=true` and a `targetOutputDir` prop:

```bash
cd "$MODELS_DIR"
STAGING_DIR="$(mktemp -d)"
OVERLAYS_PATH="${SDK_DIR}/pyatlan_v9/model/assets/_overlays/"

pkl eval typedefs/*.pkl -m "$STAGING_DIR" \
  -p sdkOnly=true \
  -p targetOutputDir=pyatlan_v9/model/assets/ \
  -p internalPackage=pyatlan_v9.model \
  -p sdkOverlaysBasePath="$OVERLAYS_PATH"
```

- Output lands at `${STAGING_DIR}/pyatlan_v9/model/assets/` (flat — no `core/` split).
- `sdkOverlaysBasePath` must be absolute — Pkl resolves `read?()` relative to the module, not CWD.
- BLDX-708's overlay system applies the hand-written method bodies (creator,
  updater, validators) during generation, so overlaid files (connection,
  atlas_glossary, data_quality_rule, persona, purpose, …) come out correct — no
  rsync exclusion needed for them (unlike the old master flow).
- A clean run writes ~667 files and every generated asset contains
  `def validate` / `def minimize` / `def relate`.

### 3. Sync into the SDK (no `--delete`)

```bash
rsync -a --exclude='_overlays' --exclude='_overlays/**' \
  --exclude='__pycache__' --exclude='*.pyc' \
  "${STAGING_DIR}/pyatlan_v9/model/assets/" \
  "${SDK_DIR}/pyatlan_v9/model/assets/"
rm -rf "${STAGING_DIR}"
```

**No `--delete`** — passthrough types (`passthrough = true` in the typedef) are
NOT generated and must be preserved: `azure_event_hub.py`,
`azure_event_consumer_group.py`, `badge.py`, `badge_condition.py`,
`snowflake_dynamic_table.py`, plus `_init_manual.py`, `relations/`, `_overlays/`.

Then remove **stale generated orphans** by hand — files a previous/renamed
generator left behind that the current typedefs no longer produce, e.g.:
- renamed: `cognite3_d_model.py` → now `cognite3d_model.py`
- retired: `business_policy_{log,exception,incident}.py`

Confirm an orphan is truly stale (not passthrough) before deleting:
`grep -n "passthrough = true" ../models/typedefs/<Module>.pkl` near its `[Type]` key.

### 4. Post-sync patches (hand-managed base files)

**`entity.py` and `referenceable.py`** carry hand-written patches the overlay
system does not fully reproduce. Restore them from the SDK's committed version
and re-apply any needed renderer fix on top:
```bash
git checkout HEAD -- pyatlan_v9/model/assets/entity.py pyatlan_v9/model/assets/referenceable.py
```
- `entity.py` `AtlasClassification`: keep `type_name: Union[Any, UnsetType]` plus
  the AtlanTagName-translation fields (`source_tag_attachments`, `tag_id`,
  `restrict_propagation_through_{lineage,hierarchy}`) — dropping them breaks
  `tests_v9/unit/test_atlan_tag_name.py`.
- `entity.py` `Entity.custom_attributes`: keep it permissive —
  `Union[Dict[str, Any], None, UnsetType]` (the master renderer fix). `Dict[str, str]`
  makes msgspec reject entities whose custom-attribute values are ints/bools/null.

**`connection.py`** — `internalPackage` rewrites the overlay's helper import into a
self-import. Fix it to point at the pydantic package where the helper lives:
```python
from pyatlan.model.assets.connection import _validate_connector_type_value
```

**`_init_manual.py`** — the hand-written registry of passthrough types. Keep ONLY
types BLDX-708 does not generate (currently `AzureEventHub`,
`AzureEventHubConsumerGroup`, `Badge`, `BadgeCondition`, `SnowflakeDynamicTable`).
When a type moves from passthrough to generated (e.g. `Cognite3DModel`), remove it
here AND from the `_init_manual` group in `__init__.py` / `__init__.pyi`, or the
lazy loader looks for it in the wrong module.

### 5. Ruff: fix, sort imports, format

```bash
cd "${SDK_DIR}"
uv run ruff check --fix --select F401,F811 pyatlan_v9/
uv run ruff check --fix --select I pyatlan_v9/     # isort — do NOT skip this
uv run ruff format pyatlan_v9/
```

The repo's default ruff `select` does not include `I`, so import sorting is a
separate explicit pass. Skipping it leaves generated imports unsorted (and can
surface load-order circular imports).

### 6. Run tests (if args contain "test")

```bash
cd "${SDK_DIR}" && uv run pytest tests_v9/unit/ -q
```

### 7. Report summary

Report: files generated/synced, orphans removed, whether `validate/minimize/relate`
are present on all assets (`asset_methods_test.py`), and test results.

## Notes

- Cloned from `git@github.com:atlanhq/models.git`; BLDX-708 = models PR #1899.
- Overlay files (custom `creator()`, `updater()`, validators) live at
  `pyatlan_v9/model/assets/_overlays/` in this repo.
- `useSetType=true` fields generate `set[str]` (user/group/role fields).
