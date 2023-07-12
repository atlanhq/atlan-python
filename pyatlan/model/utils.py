from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pyatlan.model.enums import AnnouncementType

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.dataclasses import dataclass


@dataclass
class Announcement:
    announcement_title: str
    announcement_message: Optional[str]
    announcement_type: AnnouncementType
