from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class SnapshotType(str, Enum):
    SINGLE = "single"
    PRE = "pre"
    POST = "post"


class Snapshot(BaseModel):
    id: int
    type: SnapshotType
    date: datetime
    user: str
    description: str
    cleanup: Optional[str] = None
    config: str

    class Config:
        use_enum_values = True


class SnapperConfig(BaseModel):
    name: str
    subvolume: str
    fstype: str = "btrfs"
    
    
class RetentionPolicy(BaseModel):
    hourly: int = Field(default=6, ge=0)
    daily: int = Field(default=7, ge=0)
    weekly: int = Field(default=4, ge=0)
    monthly: int = Field(default=3, ge=0)
    yearly: int = Field(default=0, ge=0)


class SystemCheck(BaseModel):
    name: str
    status: str  # OK, WARN, ERROR
    message: str


class Statistics(BaseModel):
    total_snapshots: int
    disk_usage_mb: float
    oldest_snapshot: Optional[datetime] = None
    newest_snapshot: Optional[datetime] = None
    snapshots_by_config: dict[str, int]
