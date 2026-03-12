from typing import List
from btrfs_manager.domain.models import SnapperConfig
from btrfs_manager.infrastructure.snapper_adapter import SnapperAdapter
from btrfs_manager.infrastructure.btrfs_adapter import BtrfsAdapter
from btrfs_manager.utils.logger import get_logger

logger = get_logger()


class ConfigService:
    
    def __init__(self):
        self.snapper = SnapperAdapter()
        self.btrfs = BtrfsAdapter()
    
    def list_configs(self) -> List[SnapperConfig]:
        return self.snapper.list_configs()
    
    def create_config(self, name: str, subvolume: str) -> None:
        self.snapper.create_config(name, subvolume)
    
    def auto_detect_subvolumes(self) -> List[dict]:
        return self.btrfs.list_subvolumes("/")
    
    def init_configs(self) -> None:
        existing_configs = {c.name for c in self.list_configs()}
        subvolumes = self.auto_detect_subvolumes()
        
        for subvol in subvolumes:
            if subvol["name"] not in existing_configs:
                try:
                    self.create_config(subvol["name"], subvol["path"])
                    logger.info(f"Created config {subvol['name']} for {subvol['path']}")
                except Exception as e:
                    logger.error(f"Failed to create config {subvol['name']}: {e}")
