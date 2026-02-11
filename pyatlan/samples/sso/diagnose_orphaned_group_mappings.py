# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Diagnostic and cleanup utility for orphaned SSO group mappings.

This script helps diagnose and resolve issues where Okta Push Groups fails
with stale externalId errors. This typically happens when:
1. An SSO group mapping is deleted but Okta still references the old externalId
2. A group is recreated with the same name but Okta pushes with old externalId
3. Unlinking and re-linking groups doesn't clear the orphaned mapping

Usage:
    # Diagnose orphaned mappings
    python diagnose_orphaned_group_mappings.py --mode diagnose --sso-alias <sso_alias>
    
    # Diagnose specific group
    python diagnose_orphaned_group_mappings.py --mode diagnose --sso-alias <sso_alias> --group-name <group_name>
    
    # Clean up orphaned mappings (interactive)
    python diagnose_orphaned_group_mappings.py --mode cleanup --sso-alias <sso_alias>
    
    # List all SSO group mappings
    python diagnose_orphaned_group_mappings.py --mode list --sso-alias <sso_alias>

Environment Variables:
    ATLAN_BASE_URL: Base URL of your Atlan tenant (e.g., https://apex.atlan.com)
    ATLAN_API_KEY: API key for authentication
"""

import argparse
import logging
import sys
from typing import Dict, List, Optional, Set

from pyatlan.client.atlan import AtlanClient
from pyatlan.errors import AtlanError
from pyatlan.model.group import AtlanGroup
from pyatlan.model.sso import SSOMapper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class SSOGroupMappingDiagnostic:
    """Utility to diagnose and clean up orphaned SSO group mappings."""

    def __init__(self, client: AtlanClient):
        self.client = client

    def get_all_groups(self) -> Dict[str, AtlanGroup]:
        """
        Retrieve all Atlan groups.
        
        :returns: Dictionary mapping group ID to AtlanGroup
        """
        logger.info("Retrieving all Atlan groups...")
        groups = {}
        
        try:
            response = self.client.group.get_all(limit=100)
            for group in response:
                if group.id:
                    groups[group.id] = group
            logger.info(f"Found {len(groups)} Atlan groups")
        except AtlanError as e:
            logger.error(f"Error retrieving groups: {e}")
            raise
        
        return groups

    def get_all_sso_mappings(self, sso_alias: str) -> List[SSOMapper]:
        """
        Retrieve all SSO group mappings for a given SSO provider.
        
        :param sso_alias: SSO provider alias (e.g., 'okta', 'azure', 'jumpcloud')
        :returns: List of SSO group mappings
        """
        logger.info(f"Retrieving SSO group mappings for '{sso_alias}'...")
        
        try:
            mappings = self.client.sso.get_all_group_mappings(sso_alias=sso_alias)
            logger.info(f"Found {len(mappings)} SSO group mappings")
            return mappings
        except AtlanError as e:
            logger.error(f"Error retrieving SSO mappings: {e}")
            raise

    def diagnose_orphaned_mappings(
        self, sso_alias: str, target_group_name: Optional[str] = None
    ) -> Dict[str, List[SSOMapper]]:
        """
        Diagnose orphaned SSO group mappings.
        
        An orphaned mapping is one where:
        - The mapping references a group ID that doesn't exist
        - The mapping's group name doesn't match the actual group name
        
        :param sso_alias: SSO provider alias
        :param target_group_name: Optional specific group name to check
        :returns: Dictionary with 'orphaned' and 'valid' mapping lists
        """
        logger.info("=" * 80)
        logger.info("DIAGNOSING SSO GROUP MAPPINGS")
        logger.info("=" * 80)
        
        groups = self.get_all_groups()
        mappings = self.get_all_sso_mappings(sso_alias)
        
        # Create reverse lookup: group name -> group ID
        group_name_to_id = {g.name: g.id for g in groups.values() if g.name}
        
        orphaned = []
        valid = []
        suspicious = []
        
        logger.info("\nAnalyzing mappings...")
        logger.info("-" * 80)
        
        for mapping in mappings:
            if not mapping.name or not mapping.config or not mapping.config.group_name:
                logger.warning(f"⚠️  Mapping {mapping.id} has incomplete data")
                suspicious.append(mapping)
                continue
            
            # Extract group ID from mapping name (format: <group_id>--<timestamp>)
            mapping_group_id = mapping.name.split("--")[0] if "--" in mapping.name else None
            mapped_group_name = mapping.config.group_name
            
            # Skip if target group specified and this isn't it
            if target_group_name and mapped_group_name != target_group_name:
                continue
            
            # Check if this is orphaned
            is_orphaned = False
            orphan_reason = []
            
            # Case 1: Group ID in mapping doesn't exist
            if mapping_group_id and mapping_group_id not in groups:
                is_orphaned = True
                orphan_reason.append(f"Group ID '{mapping_group_id}' not found")
            
            # Case 2: Group name doesn't match any existing group
            if mapped_group_name not in group_name_to_id:
                is_orphaned = True
                orphan_reason.append(f"Group name '{mapped_group_name}' not found")
            
            # Case 3: Group ID in mapping doesn't match current group with that name
            elif mapping_group_id and group_name_to_id.get(mapped_group_name) != mapping_group_id:
                is_orphaned = True
                current_id = group_name_to_id.get(mapped_group_name)
                orphan_reason.append(
                    f"Group ID mismatch: mapping has '{mapping_group_id}' "
                    f"but current group has '{current_id}'"
                )
            
            if is_orphaned:
                orphaned.append(mapping)
                logger.warning(f"🔴 ORPHANED: {mapping.id}")
                logger.warning(f"   Mapping Name: {mapping.name}")
                logger.warning(f"   Group Name: {mapped_group_name}")
                logger.warning(f"   SSO Group: {mapping.config.attribute_value}")
                logger.warning(f"   Reason: {', '.join(orphan_reason)}")
                logger.warning("")
            else:
                valid.append(mapping)
                if target_group_name:
                    logger.info(f"✅ VALID: {mapping.id}")
                    logger.info(f"   Mapping Name: {mapping.name}")
                    logger.info(f"   Group Name: {mapped_group_name}")
                    logger.info(f"   SSO Group: {mapping.config.attribute_value}")
                    logger.info("")
        
        logger.info("=" * 80)
        logger.info("SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Total mappings: {len(mappings)}")
        logger.info(f"✅ Valid mappings: {len(valid)}")
        logger.info(f"🔴 Orphaned mappings: {len(orphaned)}")
        logger.info(f"⚠️  Suspicious mappings: {len(suspicious)}")
        logger.info("=" * 80)
        
        return {
            "orphaned": orphaned,
            "valid": valid,
            "suspicious": suspicious,
        }

    def list_all_mappings(self, sso_alias: str) -> None:
        """
        List all SSO group mappings in a readable format.
        
        :param sso_alias: SSO provider alias
        """
        logger.info("=" * 80)
        logger.info(f"SSO GROUP MAPPINGS FOR '{sso_alias}'")
        logger.info("=" * 80)
        
        mappings = self.get_all_sso_mappings(sso_alias)
        
        if not mappings:
            logger.info("No SSO group mappings found")
            return
        
        for i, mapping in enumerate(mappings, 1):
            logger.info(f"\n{i}. Mapping ID: {mapping.id}")
            logger.info(f"   Mapping Name: {mapping.name}")
            if mapping.config:
                logger.info(f"   Atlan Group: {mapping.config.group_name}")
                logger.info(f"   SSO Group: {mapping.config.attribute_value}")
                logger.info(f"   Sync Mode: {mapping.config.sync_mode}")
            logger.info(f"   Provider: {mapping.identity_provider_alias}")
            logger.info(f"   Mapper Type: {mapping.identity_provider_mapper}")
        
        logger.info("\n" + "=" * 80)

    def cleanup_orphaned_mappings(
        self, sso_alias: str, interactive: bool = True
    ) -> int:
        """
        Clean up orphaned SSO group mappings.
        
        :param sso_alias: SSO provider alias
        :param interactive: If True, ask for confirmation before each deletion
        :returns: Number of mappings deleted
        """
        logger.info("=" * 80)
        logger.info("CLEANUP MODE")
        logger.info("=" * 80)
        
        results = self.diagnose_orphaned_mappings(sso_alias)
        orphaned = results["orphaned"]
        
        if not orphaned:
            logger.info("\n✅ No orphaned mappings found. Nothing to clean up!")
            return 0
        
        logger.warning(f"\n⚠️  Found {len(orphaned)} orphaned mapping(s) to clean up")
        
        deleted_count = 0
        
        for mapping in orphaned:
            if interactive:
                logger.info("\n" + "-" * 80)
                logger.info(f"Mapping ID: {mapping.id}")
                logger.info(f"Mapping Name: {mapping.name}")
                if mapping.config:
                    logger.info(f"Group Name: {mapping.config.group_name}")
                    logger.info(f"SSO Group: {mapping.config.attribute_value}")
                
                response = input("\nDelete this mapping? (y/n): ").strip().lower()
                
                if response != 'y':
                    logger.info("Skipped")
                    continue
            
            try:
                logger.info(f"Deleting mapping {mapping.id}...")
                self.client.sso.delete_group_mapping(
                    sso_alias=sso_alias,
                    group_map_id=mapping.id,
                )
                logger.info(f"✅ Successfully deleted mapping {mapping.id}")
                deleted_count += 1
            except AtlanError as e:
                logger.error(f"❌ Error deleting mapping {mapping.id}: {e}")
        
        logger.info("\n" + "=" * 80)
        logger.info(f"Cleanup complete. Deleted {deleted_count} orphaned mapping(s)")
        logger.info("=" * 80)
        
        return deleted_count


def main():
    """Main entry point for the diagnostic script."""
    parser = argparse.ArgumentParser(
        description="Diagnose and clean up orphaned SSO group mappings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    
    parser.add_argument(
        "--mode",
        required=True,
        choices=["diagnose", "cleanup", "list"],
        help="Operation mode: diagnose (check for issues), cleanup (remove orphaned mappings), or list (show all mappings)",
    )
    
    parser.add_argument(
        "--sso-alias",
        required=True,
        help="SSO provider alias (e.g., 'okta', 'azure', 'jumpcloud')",
    )
    
    parser.add_argument(
        "--group-name",
        help="Optional: Specific Atlan group name to diagnose",
    )
    
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Run cleanup without prompting for confirmation (dangerous!)",
    )
    
    args = parser.parse_args()
    
    # Initialize client
    try:
        client = AtlanClient()
        logger.info(f"Connected to Atlan at {client.base_url}")
    except Exception as e:
        logger.error(f"Failed to initialize Atlan client: {e}")
        logger.error("Make sure ATLAN_BASE_URL and ATLAN_API_KEY are set")
        sys.exit(1)
    
    # Initialize diagnostic tool
    diagnostic = SSOGroupMappingDiagnostic(client)
    
    # Execute requested mode
    try:
        if args.mode == "list":
            diagnostic.list_all_mappings(args.sso_alias)
        
        elif args.mode == "diagnose":
            results = diagnostic.diagnose_orphaned_mappings(
                sso_alias=args.sso_alias,
                target_group_name=args.group_name,
            )
            
            if results["orphaned"]:
                logger.info("\n💡 TIP: Run with --mode cleanup to remove orphaned mappings")
                sys.exit(1)  # Exit with error code if orphaned mappings found
        
        elif args.mode == "cleanup":
            if args.non_interactive:
                logger.warning("⚠️  Running in non-interactive mode!")
                logger.warning("⚠️  All orphaned mappings will be deleted automatically!")
                response = input("Are you sure you want to continue? (yes/no): ").strip().lower()
                if response != "yes":
                    logger.info("Cleanup cancelled")
                    sys.exit(0)
            
            deleted = diagnostic.cleanup_orphaned_mappings(
                sso_alias=args.sso_alias,
                interactive=not args.non_interactive,
            )
            
            if deleted > 0:
                logger.info("\n✅ Cleanup complete!")
                logger.info("\n💡 NEXT STEPS:")
                logger.info("1. In Okta, try unlinking and re-linking the affected group")
                logger.info("2. Use 'Link Group' (not 'Create') when re-linking")
                logger.info("3. The group push should now work without the stale externalId error")
    
    except KeyboardInterrupt:
        logger.info("\n\nOperation cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"\n❌ Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
