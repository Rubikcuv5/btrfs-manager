from typing import List, Optional
from btrfs_manager.domain.models import Snapshot
from btrfs_manager.infrastructure.snapper_adapter import SnapperAdapter
from btrfs_manager.infrastructure.btrfs_adapter import BtrfsAdapter
from btrfs_manager.utils.exceptions import InvalidOperationError, SnapshotNotFoundError
from btrfs_manager.utils.logger import get_logger

logger = get_logger()


class SnapshotService:
    
    def __init__(self):
        self.snapper = SnapperAdapter()
        self.btrfs = BtrfsAdapter()
    
    def list_snapshots(self, config: str) -> List[Snapshot]:
        return self.snapper.list_snapshots(config)
    
    def create_snapshot(self, config: str, description: str) -> int:
        return self.snapper.create_snapshot(config, description)
    
    def delete_snapshot(self, config: str, snapshot_id: int, force: bool = False) -> None:
        if snapshot_id == 0 and not force:
            raise InvalidOperationError("Cannot delete snapshot 0")
        
        snapshots = self.snapper.list_snapshots(config)
        current = [s for s in snapshots if s.id == snapshot_id]
        if not current and not force:
            raise SnapshotNotFoundError(f"Snapshot {snapshot_id} not found")
        
        self.snapper.delete_snapshot(config, snapshot_id)
    
    def get_snapshot(self, config: str, snapshot_id: int) -> Optional[Snapshot]:
        return self.snapper.get_snapshot(config, snapshot_id)
    
    def rollback_snapshot(self, config: str, snapshot_id: int) -> None:
        snapshot = self.get_snapshot(config, snapshot_id)
        if not snapshot:
            raise SnapshotNotFoundError(f"Snapshot {snapshot_id} not found")
        logger.warning(f"Rolling back to snapshot {snapshot_id}")
        # Snapper rollback logic would go here
        # subprocess.run(["snapper", "-c", config, "rollback", str(snapshot_id)], check=True)
    
    def export_snapshot(self, config: str, snapshot_id: int, output_file: str) -> None:
        snapshot = self.get_snapshot(config, snapshot_id)
        if not snapshot:
            raise SnapshotNotFoundError(f"Snapshot {snapshot_id} not found")
        
        snapshot_path = f"/.snapshots/{snapshot_id}/snapshot"
        self.btrfs.send_snapshot(snapshot_path, output_file)
    
    def import_snapshot(self, input_file: str, target_path: str = "/.snapshots") -> None:
        self.btrfs.receive_snapshot(input_file, target_path)
