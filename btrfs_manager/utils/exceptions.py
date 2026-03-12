class BtrfsManagerError(Exception):
    """Base exception"""
    pass


class SnapperNotFoundError(BtrfsManagerError):
    """Snapper not installed"""
    pass


class BtrfsNotFoundError(BtrfsManagerError):
    """BTRFS filesystem not found"""
    pass


class PermissionError(BtrfsManagerError):
    """Insufficient permissions"""
    pass


class SnapshotNotFoundError(BtrfsManagerError):
    """Snapshot does not exist"""
    pass


class ConfigNotFoundError(BtrfsManagerError):
    """Configuration not found"""
    pass


class InvalidOperationError(BtrfsManagerError):
    """Operation not allowed"""
    pass
