# SSO Group Mapping Utilities

This directory contains utilities for managing SSO (Single Sign-On) group mappings in Atlan.

## Available Tools

### Diagnose Orphaned Group Mappings

**File:** `diagnose_orphaned_group_mappings.py`

A diagnostic and cleanup utility for identifying and resolving orphaned SSO group mappings that can cause Okta Push Groups to fail with stale `externalId` errors.

#### Quick Start

```bash
# Set up environment
export ATLAN_BASE_URL="https://your-tenant.atlan.com"
export ATLAN_API_KEY="your-api-key"

# Diagnose all SSO group mappings
python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
  --mode diagnose \
  --sso-alias okta

# Diagnose a specific group
python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
  --mode diagnose \
  --sso-alias okta \
  --group-name grpAtlanProdWorkflowAdmin

# Clean up orphaned mappings (interactive)
python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
  --mode cleanup \
  --sso-alias okta

# List all SSO group mappings
python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
  --mode list \
  --sso-alias okta
```

#### Common Use Cases

1. **Okta Push Groups Failing with Stale externalId**
   - Run diagnostic to identify orphaned mappings
   - Clean up orphaned mappings
   - In Okta, unlink and re-link the group (use "Link Group", not "Create")

2. **Regular Maintenance**
   - Periodically run diagnostic to catch orphaned mappings early
   - Schedule as part of your regular Atlan maintenance routine

3. **Group Migration or Cleanup**
   - Before deleting groups, check for associated SSO mappings
   - Clean up mappings before deleting the group to avoid orphans

#### Options

- `--mode`: Operation mode
  - `diagnose`: Check for orphaned mappings (recommended first step)
  - `cleanup`: Remove orphaned mappings (interactive by default)
  - `list`: Display all SSO group mappings

- `--sso-alias`: SSO provider alias (e.g., `okta`, `azure`, `jumpcloud`)

- `--group-name`: (Optional) Check only a specific group

- `--non-interactive`: Run cleanup without prompting (use with caution!)

## Documentation

For detailed information about SSO group mapping troubleshooting, see:
- [SSO Troubleshooting Guide](../../../docs/sso_troubleshooting.md)
- [SSO Client API Documentation](../../../docs/client/sso.rst)

## Support

If you encounter issues or need help:

1. Run the diagnostic script and save the output
2. Check the [SSO Troubleshooting Guide](../../../docs/sso_troubleshooting.md)
3. If the issue persists, contact Atlan Support with:
   - Diagnostic output
   - Full error messages
   - Steps you've already tried

## Related Issues

- **LINTEST-425**: Okta Push Groups stale externalId / orphaned mapping issue
