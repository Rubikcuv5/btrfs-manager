import subprocess
import re
from datetime import datetime
from typing import List, Optional
from btrfs_manager.domain.models import Snapshot, SnapshotType, SnapperConfig
from btrfs_manager.utils.exceptions import SnapperNotFoundError, ConfigNotFoundError, SnapshotNotFoundError
from btrfs_manager.utils.logger import get_logger

logger = get_logger()


class SnapperAdapter:
    
    def check_installed(self) -> bool:
        try:
            subprocess.run(["snapper", "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def list_configs(self) -> List[SnapperConfig]:
        result = subprocess.run(["snapper", "list-configs"], capture_output=True, text=True, check=True)
        configs = []
        for line in result.stdout.strip().split("\n")[2:]:
            parts = line.split("|")
            if len(parts) >= 2:
                configs.append(SnapperConfig(name=parts[0].strip(), subvolume=parts[1].strip()))
        return configs
    
    def create_config(self, name: str, subvolume: str) -> None:
        subprocess.run(["snapper", "-c", name, "create-config", subvolume], check=True)
        logger.info(f"Created config {name} for {subvolume}")
    
    def list_snapshots(self, config: str) -> List[Snapshot]:
        result = subprocess.run(["snapper", "-c", config, "list"], capture_output=True, text=True, check=True)
        snapshots = []
        for line in result.stdout.strip().split("\n")[2:]:
            parts = re.split(r'\s+\|\s+', line.strip())
            if len(parts) >= 5:
                snapshots.append(Snapshot(
                    id=int(parts[0]),
                    type=SnapshotType(parts[1].lower()),
                    date=datetime.strptime(parts[2], "%Y-%m-%d %H:%M:%S"),
                    user=parts[3],
                    description=parts[4] if len(parts) > 4 else "",
                    config=config
                ))
        return snapshots
    
    def create_snapshot(self, config: str, description: str) -> int:
        result = subprocess.run(["snapper", "-c", config, "create", "-d", description], capture_output=True, text=True, check=True)
        match = re.search(r'(\d+)', result.stdout)
        snapshot_id = int(match.group(1)) if match else 0
        logger.info(f"Created snapshot {snapshot_id} for {config}")
        return snapshot_id
    
    def delete_snapshot(self, config: str, snapshot_id: int) -> None:
        if snapshot_id == 0:
            raise SnapshotNotFoundError("Cannot delete snapshot 0")
        subprocess.run(["snapper", "-c", config, "delete", str(snapshot_id)], check=True)
        logger.info(f"Deleted snapshot {snapshot_id} from {config}")
    
    def get_snapshot(self, config: str, snapshot_id: int) -> Optional[Snapshot]:
        snapshots = self.list_snapshots(config)
        for snap in snapshots:
            if snap.id == snapshot_id:
                return snap
        return None
