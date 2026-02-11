# LINTEST-410 Repository Mismatch

## Issue Summary
**Title:** Data preview panel doesn't update when doing a test run from node (copy)

**Issue ID:** LINTEST-410

## Problem Identified

This issue has been assigned to the **wrong repository**.

### Evidence

1. **Issue describes frontend/UI components:**
   - Data preview panel
   - Graph nodes with test run buttons
   - Property panel interactions
   - TypeScript file: `usePreviewData.ts` in `property-panel/preview-panel/hooks/`

2. **Screenshot shows:**
   - URL: `datamesh2.atlan.com/automation/editor/`
   - Workflow automation editor UI
   - SQL query editor
   - Graph-based workflow nodes

3. **Current repository:**
   - Repository: `atlan-python`
   - Language: Python
   - Purpose: Python SDK for Atlan API
   - No frontend/TypeScript code exists

### Correct Repository

Based on the evidence, this issue should be assigned to the **Atlan frontend/automation editor repository** which contains:
- TypeScript/React codebase
- Workflow/automation editor UI
- Property panel components
- Preview panel hooks

### Issue Details (for correct repository)

**Primary Bug:**
- Steps to reproduce:
  1. Do a Test run on any node via Property Panel → See results preview panel
  2. Do another test run via graph node Test button → results preview panel doesn't update

**Secondary Bug:**
- Test run button on graph node is disabled but no tooltip appears (inconsistent with other execution buttons)

**Referenced Files:**
- `property-panel/preview-panel/hooks/usePreviewData.ts` (line 226)

**Related Issues:**
- AUT-487 (similar preview panel update issue)
- PR #335 (attempted fix for similar issue)

## Recommendation

Please reassign this issue to the correct frontend repository that contains the automation/workflow editor codebase.
