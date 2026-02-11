# Support Guide: Resolving Orphaned SSO Group Mappings

**Issue Type:** Okta Push Groups / SCIM Group Provisioning Failures  
**Error Pattern:** "stale externalId" or "orphaned mapping"  
**Severity:** Medium - Blocks specific group from being provisioned  
**Related:** LINTEST-425

## Quick Reference

### Symptoms Checklist

- [ ] Customer reports Okta Push Groups failing for a specific group
- [ ] Error message mentions "externalId" or "unable to get the group"
- [ ] Other groups with similar settings work fine
- [ ] Issue persists after unlinking/re-linking in Okta
- [ ] Issue persists after deleting and recreating the Atlan group

If 3+ of these apply, this is likely an orphaned SSO mapping issue.

### Quick Resolution (5 minutes)

```bash
# 1. Set up environment
export ATLAN_BASE_URL="https://customer-tenant.atlan.com"
export ATLAN_API_KEY="<support-api-key>"

# 2. Run diagnostic
python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
  --mode diagnose \
  --sso-alias okta \
  --group-name <affected-group-name>

# 3. If orphaned mapping found, clean it up
python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
  --mode cleanup \
  --sso-alias okta

# 4. Verify cleanup
python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
  --mode diagnose \
  --sso-alias okta \
  --group-name <affected-group-name>
```

## Detailed Resolution Steps

### Step 1: Gather Information

Collect the following from the customer:

1. **Tenant Details:**
   - Tenant URL (e.g., `https://apex.atlan.com`)
   - Affected group name (e.g., `grpAtlanProdWorkflowAdmin`)
   - SSO provider (Okta, Azure AD, JumpCloud, etc.)

2. **Error Details:**
   - Full error message from the SSO provider
   - Screenshot of the error (if available)
   - When did the issue start?

3. **What Has Been Tried:**
   - Have they unlinked/re-linked the group?
   - Have they deleted and recreated the Atlan group?
   - Are there any recent changes to SSO configuration?

### Step 2: Run Diagnostics

#### Option A: Using the Python SDK (Recommended)

```bash
# Install pyatlan if not already available
pip install pyatlan

# Set environment variables
export ATLAN_BASE_URL="https://customer-tenant.atlan.com"
export ATLAN_API_KEY="<support-api-key>"

# Run diagnostic for the specific group
python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
  --mode diagnose \
  --sso-alias okta \
  --group-name grpAtlanProdWorkflowAdmin
```

**Expected Output:**

If orphaned mapping exists:
```
🔴 ORPHANED: mapping-id-123
   Mapping Name: group-id-old--1234567890
   Group Name: grpAtlanProdWorkflowAdmin
   SSO Group: grpAtlanProdWorkflowAdmin
   Reason: Group ID mismatch: mapping has 'group-id-old' but current group has 'group-id-new'
```

If no issues found:
```
✅ VALID: mapping-id-456
   Mapping Name: group-id-current--1234567891
   Group Name: grpAtlanProdWorkflowAdmin
   SSO Group: grpAtlanProdWorkflowAdmin
```

#### Option B: Manual API Check

```bash
# Get all SSO mappings
curl -X GET \
  "${ATLAN_BASE_URL}/api/service/auth/admin/realms/default/identity-provider/instances/okta/mappers" \
  -H "Authorization: Bearer ${ATLAN_API_KEY}"

# Get all groups
curl -X GET \
  "${ATLAN_BASE_URL}/api/service/groups" \
  -H "Authorization: Bearer ${ATLAN_API_KEY}"
```

### Step 3: Clean Up Orphaned Mappings

#### Automated Cleanup (Recommended)

```bash
# Interactive cleanup (asks for confirmation)
python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
  --mode cleanup \
  --sso-alias okta

# Non-interactive (use with caution)
python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
  --mode cleanup \
  --sso-alias okta \
  --non-interactive
```

#### Manual Cleanup

If you prefer to delete specific mappings manually:

```python
from pyatlan.client.atlan import AtlanClient

client = AtlanClient()

# Delete the orphaned mapping
client.sso.delete_group_mapping(
    sso_alias="okta",
    group_map_id="mapping-id-to-delete"
)

print("✅ Deleted orphaned mapping")
```

Or via REST API:

```bash
curl -X POST \
  "${ATLAN_BASE_URL}/api/service/auth/admin/realms/default/identity-provider/instances/okta/mappers/${MAPPING_ID}/delete" \
  -H "Authorization: Bearer ${ATLAN_API_KEY}"
```

### Step 4: Verify and Re-link in Okta

After cleaning up the orphaned mapping:

1. **Verify the Atlan group exists:**
   ```bash
   python -c "
   from pyatlan.client.atlan import AtlanClient
   client = AtlanClient()
   groups = client.group.get_by_name(alias='grpAtlanProdWorkflowAdmin')
   if groups and groups.records:
       print(f'✅ Group exists: {groups.records[0].id}')
   else:
       print('❌ Group not found - needs to be created')
   "
   ```

2. **In Okta:**
   - Go to Applications → Atlan → Push Groups
   - **Unlink** the affected group (do not delete in Okta)
   - **Re-link** using "Link Group" (NOT "Create")
   - Select the existing Atlan group from the dropdown

3. **Test the push:**
   - Save the push group configuration
   - Trigger a push
   - Verify the group members are synced

### Step 5: Follow-Up

1. **Run diagnostic again** to confirm no orphaned mappings remain:
   ```bash
   python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings \
     --mode diagnose \
     --sso-alias okta
   ```

2. **Check for other affected groups:**
   - If this is a widespread issue, run diagnostics without `--group-name`
   - Clean up all orphaned mappings

3. **Document the incident:**
   - Note the group name(s) affected
   - Record the orphaned mapping ID(s) that were deleted
   - Update the customer ticket with resolution details

## Common Scenarios

### Scenario 1: Group Deleted and Recreated

**Situation:** Customer deleted an Atlan group and created a new one with the same name.

**Problem:** The old SSO mapping still references the old group ID.

**Solution:**
1. Run diagnostic to identify the orphaned mapping
2. Delete the orphaned mapping
3. In Okta, unlink and re-link the group

### Scenario 2: SSO Configuration Changed

**Situation:** Customer changed SSO provider (e.g., from Azure to Okta) or reconfigured SSO.

**Problem:** Old mappings from the previous SSO configuration still exist.

**Solution:**
1. Run diagnostic for BOTH SSO providers (old and new)
2. Clean up orphaned mappings from the old provider
3. Verify mappings for the new provider are correct

### Scenario 3: Multiple Groups Affected

**Situation:** Multiple groups are experiencing the same issue.

**Problem:** Likely a systemic issue from a bulk group operation.

**Solution:**
1. Run diagnostic for all groups: `--mode diagnose --sso-alias okta`
2. Use non-interactive cleanup: `--mode cleanup --sso-alias okta --non-interactive`
3. Have customer re-link all affected groups in Okta

### Scenario 4: Recurring Issue

**Situation:** The same group keeps getting orphaned mappings.

**Problem:** Customer is likely using "Create" instead of "Link Group" in Okta, or there's an automation issue.

**Solution:**
1. Clean up the orphaned mapping
2. **Educate the customer** on proper linking procedure
3. Check if any automation or scripts are incorrectly managing groups
4. Consider creating a monitoring alert for this specific group

## Escalation Criteria

Escalate to engineering if:

- [ ] Diagnostic script fails to run or errors out
- [ ] Cleanup doesn't resolve the issue (orphaned mapping still present after deletion)
- [ ] Issue recurs immediately after cleanup
- [ ] No orphaned mappings found but the issue persists
- [ ] Backend logs show errors related to Keycloak or SCIM provisioning
- [ ] Multiple customers reporting the same issue

## Prevention Recommendations

Share these best practices with customers:

### For Support Teams

1. **Regular Audits:**
   - Run diagnostic monthly for all SSO providers
   - Clean up orphaned mappings proactively

2. **Documentation:**
   - Maintain a runbook for common SSO issues
   - Document customer's SSO configuration

3. **Monitoring:**
   - Set up alerts for SSO provisioning failures
   - Track orphaned mapping incidents

### For Customers

1. **Proper Group Deletion:**
   - Before deleting a group, unlink it from SSO first
   - Use the diagnostic script before bulk group operations

2. **Correct Linking Procedure:**
   - Always use "Link Group" (not "Create") when re-linking
   - Verify the group exists in Atlan before linking

3. **Testing:**
   - Test group pushes in a non-production tenant first
   - Verify membership sync after any SSO configuration changes

## Technical Details

### What Are Orphaned Mappings?

An SSO group mapping (Keycloak Identity Provider Mapper) creates a link between:
- An Atlan group (identified by group ID)
- An SSO group (identified by group name in the SSO provider)

When a group is deleted or recreated, the new group gets a new ID, but the old mapping still references the old ID. This is an "orphaned" mapping.

### Why Does Okta Fail?

When Okta tries to push a group:
1. Okta sends a SCIM request with the group's `externalId`
2. Atlan/Keycloak looks up the group by `externalId`
3. If the mapping is orphaned, Keycloak can't find the group
4. The push fails with "unable to get the group" error

### What Does Cleanup Do?

The cleanup process:
1. Identifies mappings that reference non-existent groups
2. Deletes these orphaned mappings from Keycloak
3. Allows Okta to create a fresh mapping on the next push

## API Reference

### Diagnostic Script

```
python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings [OPTIONS]

Options:
  --mode {diagnose,cleanup,list}  Operation mode (required)
  --sso-alias TEXT                SSO provider alias (required)
  --group-name TEXT               Specific group to check (optional)
  --non-interactive               Skip prompts in cleanup mode
```

### SSO Client Methods

```python
from pyatlan.client.atlan import AtlanClient

client = AtlanClient()

# Get all SSO group mappings
mappings = client.sso.get_all_group_mappings(sso_alias="okta")

# Get specific mapping
mapping = client.sso.get_group_mapping(
    sso_alias="okta",
    group_map_id="mapping-id"
)

# Delete mapping
client.sso.delete_group_mapping(
    sso_alias="okta",
    group_map_id="mapping-id"
)

# Create new mapping
group = client.group.get_by_name(alias="MyGroup").records[0]
new_mapping = client.sso.create_group_mapping(
    sso_alias="okta",
    atlan_group=group,
    sso_group_name="okta-group-name"
)
```

## Troubleshooting the Diagnostic Script

### Script Won't Run

**Problem:** `No module named pyatlan`

**Solution:**
```bash
pip install pyatlan
# or
pip install --upgrade pyatlan
```

### Authentication Errors

**Problem:** `401 Unauthorized` or `403 Forbidden`

**Solution:**
- Verify `ATLAN_BASE_URL` is correct (include `https://`)
- Verify `ATLAN_API_KEY` has admin permissions
- Check API key hasn't expired

### No Orphaned Mappings Found

**Problem:** Diagnostic shows all mappings as valid, but issue persists

**Possible Causes:**
- Wrong SSO alias (check if it's `okta`, `azure`, `jumpcloud`, etc.)
- Wrong group name (check exact name including capitalization)
- Issue is not related to orphaned mappings (escalate)

## Related Documentation

- [SSO Troubleshooting Guide](./sso_troubleshooting.md)
- [SSO Client API](./client/sso.rst)
- [Group Management API](./client/group.rst)

## Changelog

- **2025-02-11:** Initial support guide created for LINTEST-425
