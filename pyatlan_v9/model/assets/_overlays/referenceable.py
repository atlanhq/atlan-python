# INTERNAL_IMPORT: from pyatlan.model.lineage_ref import LineageRef

    @classmethod
    def can_be_archived(cls) -> bool:
        """
        Indicates if an asset can be archived via the asset.delete_by_guid method.
        :returns: True if archiving is supported
        """
        return True

    @property
    def assigned_terms(self):
        """
        Get assigned glossary terms (maps to Entity.meanings).

        In legacy models, assigned_terms was a property that mapped to
        attributes.meanings. In v9, meanings is a direct field on Entity.
        """
        return self.meanings if self.meanings is not UNSET else None

    @assigned_terms.setter
    def assigned_terms(self, value):
        """Set assigned glossary terms."""
        self.meanings = value
