# SSO Group Mapping Troubleshooting Guide

## Overview

This guide helps you diagnose and resolve issues with SSO (Single Sign-On) group mappings, particularly when using Okta Push Groups or similar SCIM-based group provisioning systems.

## Common Issue: Stale externalId / Orphaned Mapping

### Symptoms

When attempting to push a group from your SSO provider (e.g., Okta) to Atlan, you receive an error similar to:

```
Failed on XX-XX-XXXX XX:XX:XX PM UTC: Unable to update Group Push mapping target App group 
`<group_name>`: Error while trying to get the group `<group_name>` with the externalId 
`<uuid>` and id `com.saasure.db.dto.platform.entity.AppGroup@...`
```

### Key Indicators

- ✅ Other groups with similar settings push successfully
- ✅ The error consistently mentions a specific `externalId`
- ✅ The issue persists even after:
  - Removing the SSO group mapping in Atlan
  - Creating a new Atlan group with a matching name
  - Unlinking and re-linking the group from Okta

### Root Cause

This issue occurs when there is a **stale mapping** between your SSO provider (Okta) and Atlan. Specifically:

1. An SSO group mapping was previously created, establishing a link between an Okta group and an Atlan group
2. The Atlan group was deleted or recreated, or the SSO mapping was removed
3. However, Okta still has a record of the old `externalId` for that group
4. When Okta tries to push the group again, it uses the old `externalId` which Atlan cannot resolve

The SSO group mapping (identity provider mapper in Keycloak) is stored separately from the group itself, and deleting one doesn't automatically clean up the other.

## Diagnosis

### Using the Diagnostic Script

We provide a diagnostic utility to identify orphaned SSO group mappings. This script is part of the Python SDK.

#### Prerequisites

```bash
# Install the Atlan Python SDK
pip install pyatlan

# Set up environment variables
export ATLAN_BASE_URL="https://your-tenant.atlan.com"
export ATLAN_API_KEY="your-api-key"
```

#### Diagnose All Mappings

To check for orphaned mappings across all groups:

```bash
python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
  --mode diagnose \
  --sso-alias okta
```

#### Diagnose Specific Group

To check a specific group that's failing:

```bash
python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
  --mode diagnose \
  --sso-alias okta \
  --group-name grpAtlanProdWorkflowAdmin
```

#### List All SSO Mappings

To see all current SSO group mappings:

```bash
python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
  --mode list \
  --sso-alias okta
```

### Manual Diagnosis

If you prefer to diagnose manually using the Python SDK:

```python
from pyatlan.client.atlan import AtlanClient

# Initialize client
client = AtlanClient()

# Get all SSO group mappings
sso_alias = "okta"  # or "azure", "jumpcloud", etc.
mappings = client.sso.get_all_group_mappings(sso_alias=sso_alias)

# Get all Atlan groups
groups_response = client.group.get_all()
groups = {g.id: g for g in groups_response if g.id}

# Check each mapping
for mapping in mappings:
    if not mapping.name or not mapping.config:
        continue
    
    # Extract group ID from mapping name (format: <group_id>--<timestamp>)
    mapping_group_id = mapping.name.split("--")[0] if "--" in mapping.name else None
    
    # Check if group still exists
    if mapping_group_id and mapping_group_id not in groups:
        print(f"⚠️ ORPHANED: Mapping {mapping.id} references non-existent group {mapping_group_id}")
        print(f"   SSO Group: {mapping.config.attribute_value}")
        print(f"   Atlan Group: {mapping.config.group_name}")
```

## Resolution

### Option 1: Automated Cleanup (Recommended)

Use the diagnostic script to automatically clean up orphaned mappings:

```bash
# Interactive cleanup (prompts for confirmation for each mapping)
python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
  --mode cleanup \
  --sso-alias okta

# Non-interactive cleanup (automatically deletes all orphaned mappings)
python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
  --mode cleanup \
  --sso-alias okta \
  --non-interactive
```

**⚠️ Warning:** Non-interactive mode will delete ALL orphaned mappings without confirmation. Use with caution!

### Option 2: Manual Cleanup

#### Using the Python SDK

```python
from pyatlan.client.atlan import AtlanClient

client = AtlanClient()

# Find the orphaned mapping ID (from diagnosis step)
orphaned_mapping_id = "your-mapping-id-here"
sso_alias = "okta"

# Delete the orphaned mapping
client.sso.delete_group_mapping(
    sso_alias=sso_alias,
    group_map_id=orphaned_mapping_id
)

print(f"✅ Deleted orphaned mapping {orphaned_mapping_id}")
```

#### Using the REST API

If you need to clean up mappings directly via API:

```bash
# Get your API token and base URL
ATLAN_BASE_URL="https://your-tenant.atlan.com"
ATLAN_API_KEY="your-api-key"
SSO_ALIAS="okta"
MAPPING_ID="mapping-id-to-delete"

# Delete the mapping
curl -X POST \
  "${ATLAN_BASE_URL}/api/service/auth/admin/realms/default/identity-provider/instances/${SSO_ALIAS}/mappers/${MAPPING_ID}/delete" \
  -H "Authorization: Bearer ${ATLAN_API_KEY}" \
  -H "Content-Type: application/json"
```

### Post-Cleanup Steps

After cleaning up the orphaned mappings:

1. **In Atlan:**
   - Verify the Atlan group exists: Settings → Access → Groups
   - If needed, create the group: Settings → Access → Groups → + New Group

2. **In Okta:**
   - Go to Applications → Atlan → Push Groups
   - **Unlink** the affected group (do not delete in Okta)
   - **Re-link** the group using "Link Group" (NOT "Create")
   - Choose the existing Atlan group from the dropdown

3. **Test:**
   - Try pushing the group again
   - The error should now be resolved
   - Verify group membership is correctly synced

## Prevention

To prevent this issue in the future:

### 1. Proper Group Deletion Workflow

When deleting a group that has SSO mapping:

```python
from pyatlan.client.atlan import AtlanClient

client = AtlanClient()
sso_alias = "okta"
group_id = "group-guid-here"

# Step 1: Find and delete SSO mappings first
all_mappings = client.sso.get_all_group_mappings(sso_alias=sso_alias)
for mapping in all_mappings:
    if mapping.name and group_id in mapping.name:
        print(f"Deleting SSO mapping: {mapping.id}")
        client.sso.delete_group_mapping(
            sso_alias=sso_alias,
            group_map_id=mapping.id
        )

# Step 2: Then delete the group
client.group.purge(guid=group_id)
print(f"✅ Group and SSO mappings deleted successfully")
```

### 2. Re-linking Groups

When re-linking a group after unlinking:

- ✅ **DO:** Use "Link Group" and select the existing Atlan group
- ❌ **DON'T:** Use "Create" which creates a new group and new mapping
- ❌ **DON'T:** Delete and recreate the Atlan group without cleaning up SSO mappings

### 3. Regular Audits

Periodically run the diagnostic script to identify orphaned mappings:

```bash
# Add to your maintenance routine
python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
  --mode diagnose \
  --sso-alias okta
```

## Advanced Scenarios

### Multiple SSO Providers

If you have multiple SSO providers (e.g., Okta and Azure AD), run diagnostics for each:

```bash
for sso in okta azure jumpcloud; do
  echo "Checking $sso..."
  python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
    --mode diagnose \
    --sso-alias $sso
done
```

### Scripted Cleanup

For large-scale cleanups across multiple tenants:

```python
from pyatlan.client.atlan import AtlanClient
from pyatlan.samples.sso.diagnose_orphaned_group_mappings import SSOGroupMappingDiagnostic

# Initialize
client = AtlanClient()
diagnostic = SSOGroupMappingDiagnostic(client)

# Run diagnosis
results = diagnostic.diagnose_orphaned_mappings(sso_alias="okta")

# Automated cleanup (be careful!)
if results["orphaned"]:
    print(f"Found {len(results['orphaned'])} orphaned mappings")
    deleted = diagnostic.cleanup_orphaned_mappings(
        sso_alias="okta",
        interactive=False  # Automatic deletion
    )
    print(f"Deleted {deleted} mappings")
```

### Monitoring and Alerting

Set up monitoring to detect this issue early:

```python
import logging
from pyatlan.client.atlan import AtlanClient
from pyatlan.samples.sso.diagnose_orphaned_group_mappings import SSOGroupMappingDiagnostic

def check_orphaned_mappings(sso_alias: str) -> bool:
    """
    Check for orphaned SSO mappings and return True if any found.
    Suitable for integration with monitoring systems.
    """
    client = AtlanClient()
    diagnostic = SSOGroupMappingDiagnostic(client)
    
    results = diagnostic.diagnose_orphaned_mappings(sso_alias=sso_alias)
    
    orphaned_count = len(results["orphaned"])
    
    if orphaned_count > 0:
        logging.warning(f"Found {orphaned_count} orphaned SSO mappings for {sso_alias}")
        return True
    
    return False

# Usage in monitoring script
if check_orphaned_mappings("okta"):
    # Send alert to your monitoring system
    # e.g., send_pagerduty_alert(), send_slack_message(), etc.
    pass
```

## API Reference

### SSO Client Methods

All SSO operations are available through `client.sso`:

```python
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.group import AtlanGroup

client = AtlanClient()

# Create a new SSO group mapping
group = client.group.get_by_name(alias="MyGroup").records[0]
mapping = client.sso.create_group_mapping(
    sso_alias="okta",
    atlan_group=group,
    sso_group_name="okta-group-name"
)

# Get all SSO group mappings
all_mappings = client.sso.get_all_group_mappings(sso_alias="okta")

# Get specific SSO group mapping
mapping = client.sso.get_group_mapping(
    sso_alias="okta",
    group_map_id="mapping-id"
)

# Update SSO group mapping
updated = client.sso.update_group_mapping(
    sso_alias="okta",
    atlan_group=group,
    group_map_id="mapping-id",
    sso_group_name="new-okta-group-name"
)

# Delete SSO group mapping
client.sso.delete_group_mapping(
    sso_alias="okta",
    group_map_id="mapping-id"
)
```

## Support Escalation

If the above steps don't resolve your issue, escalate to Atlan Support with:

1. **Environment Details:**
   - Tenant URL
   - SSO provider (Okta, Azure AD, etc.)
   - Affected group name(s)

2. **Diagnostic Output:**
   ```bash
   python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
     --mode diagnose \
     --sso-alias okta > diagnostic_output.txt
   ```

3. **Error Messages:**
   - Full error message from Okta/SSO provider
   - Any relevant logs from Atlan

4. **Steps Already Taken:**
   - List what you've already tried
   - Whether cleanup script was run
   - Results of cleanup attempts

## Related Documentation

- [SSO Group Mappings API](../client/sso.rst)
- [Group Management API](../client/group.rst)
- [Atlan SSO Configuration](https://ask.atlan.com/hc/en-us/articles/sso-setup)

## Changelog

- **2025-02-11:** Initial documentation for LINTEST-425 (Okta Push Groups stale externalId issue)
